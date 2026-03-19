#!/usr/bin/env python3
"""
猎聘 MCP CLI — 通过 MCP 协议调用猎聘求职工具

Usage:
    python liepin_mcp.py search-job --jobName "AI产品经理" --address "上海"
    python liepin_mcp.py apply-job --jobId "xxx" --jobKind "1"
    python liepin_mcp.py my-resume
    python liepin_mcp.py update-resume --module basic --data '{...}'
    python liepin_mcp.py list-tools
"""

import argparse
import json
import os
import sys
import uuid
import urllib.request
import urllib.error
from pathlib import Path

# ── 配置 ──────────────────────────────────────────────────────────────

DEFAULT_MCP_URL = "https://open-mcp.liepin.com/servers/cc4a45655fc3432eaf346555d04be77e/mcp"

CONFIG_PATH = Path.home() / ".config" / "liepin-mcp" / "config.json"


def load_config():
    """加载配置（token 等）"""
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_config(config):
    """保存配置"""
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


def get_tokens(config):
    """获取 token"""
    gateway_token = config.get("gateway_token") or os.environ.get("LIEPIN_GATEWAY_TOKEN", "")
    user_token = config.get("user_token") or os.environ.get("LIEPIN_USER_TOKEN", "")

    if not gateway_token or not user_token:
        print("错误: 未配置 token。请先运行: python liepin_mcp.py setup", file=sys.stderr)
        sys.exit(1)

    return gateway_token, user_token


# ── HTTP 请求（零依赖）────────────────────────────────────────────────

class McpSession:
    """MCP 会话管理，使用 urllib（无需 requests）"""

    def __init__(self, url, gateway_token, user_token):
        self.url = url
        self.gateway_token = gateway_token
        self.user_token = user_token
        self.session_id = None

    def _post(self, payload, timeout=30):
        """发送 POST 请求"""
        data = json.dumps(payload).encode("utf-8")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.gateway_token}",
            "x-user-token": self.user_token,
        }
        if self.session_id:
            headers["mcp-session-id"] = self.session_id

        req = urllib.request.Request(self.url, data=data, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                # 保存 session ID
                sid = resp.headers.get("mcp-session-id")
                if sid:
                    self.session_id = sid
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            print(f"HTTP {e.code}: {body}", file=sys.stderr)
            sys.exit(1)
        except urllib.error.URLError as e:
            print(f"网络错误: {e.reason}", file=sys.stderr)
            sys.exit(1)

    def initialize(self):
        """MCP 初始化握手"""
        return self._post({
            "jsonrpc": "2.0",
            "id": str(uuid.uuid4()),
            "method": "initialize",
            "params": {
                "protocolVersion": "2025-03-26",
                "capabilities": {},
                "clientInfo": {"name": "liepin-mcp-cli", "version": "1.0.0"},
            },
        })

    def list_tools(self):
        """列出所有可用工具"""
        return self._post({
            "jsonrpc": "2.0",
            "id": str(uuid.uuid4()),
            "method": "tools/list",
            "params": {},
        })

    def call_tool(self, tool_name, arguments, timeout=60):
        """调用 MCP 工具"""
        return self._post({
            "jsonrpc": "2.0",
            "id": str(uuid.uuid4()),
            "method": "tools/call",
            "params": {"name": tool_name, "arguments": arguments},
        }, timeout=timeout)


def create_session(config):
    """创建并初始化 MCP 会话"""
    url = config.get("mcp_url", DEFAULT_MCP_URL)
    gateway_token, user_token = get_tokens(config)
    session = McpSession(url, gateway_token, user_token)
    session.initialize()
    return session


# ── 命令实现 ──────────────────────────────────────────────────────────

def cmd_setup(args):
    """配置 token"""
    config = load_config()
    print("猎聘 MCP 配置向导")
    print("=" * 40)
    print("请从 https://www.liepin.com/mcp/server 获取 token\n")

    gateway_token = input("Gateway Token (mcp_gateway_token_xxx): ").strip()
    user_token = input("User Token (liepin_user_token_xxx): ").strip()

    if gateway_token:
        config["gateway_token"] = gateway_token
    if user_token:
        config["user_token"] = user_token
    config["mcp_url"] = args.url or DEFAULT_MCP_URL

    save_config(config)
    print(f"\n配置已保存到 {CONFIG_PATH}")


def cmd_list_tools(args):
    """列出可用工具"""
    config = load_config()
    session = create_session(config)
    result = session.list_tools()

    if "result" in result and "tools" in result["result"]:
        tools = result["result"]["tools"]
        if args.json:
            print(json.dumps(tools, indent=2, ensure_ascii=False))
        else:
            print(f"\n共 {len(tools)} 个可用工具:\n")
            for tool in tools:
                print(f"  {tool['name']}")
                print(f"    {tool.get('description', '无描述')}")
                if "inputSchema" in tool:
                    props = tool["inputSchema"].get("properties", {})
                    if props:
                        params = ", ".join(props.keys())
                        print(f"    参数: {params}")
                print()
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_search_job(args):
    """搜索职位"""
    config = load_config()
    session = create_session(config)

    arguments = {}
    for key in ("jobName", "address", "salary", "education", "experience", "companyType", "companyName"):
        val = getattr(args, key, None)
        if val:
            arguments[key] = val

    result = session.call_tool("user-search-job", arguments)
    _print_result(result, args.json)


def cmd_apply_job(args):
    """投递职位"""
    config = load_config()
    session = create_session(config)
    result = session.call_tool("user-apply-job", {"jobId": args.jobId, "jobKind": args.jobKind})
    _print_result(result, args.json)


def cmd_my_resume(args):
    """查看简历"""
    config = load_config()
    session = create_session(config)
    result = session.call_tool("my-resume", {})
    _print_result(result, args.json)


def cmd_update_resume(args):
    """更新简历"""
    config = load_config()
    session = create_session(config)

    arguments = {"module": args.module}
    if args.data:
        arguments["data"] = json.loads(args.data)

    result = session.call_tool("resume-toolkit", arguments)
    _print_result(result, args.json)


def cmd_call(args):
    """通用 MCP 工具调用"""
    config = load_config()
    session = create_session(config)

    arguments = json.loads(args.arguments) if args.arguments else {}
    result = session.call_tool(args.tool, arguments)
    _print_result(result, args.json)


def _print_result(result, as_json=False):
    """输出结果"""
    if "result" in result:
        content = result["result"]
        if as_json:
            print(json.dumps(content, indent=2, ensure_ascii=False))
        else:
            # MCP tool result: {"content": [{"type": "text", "text": "..."}]}
            if isinstance(content, dict) and "content" in content:
                for item in content["content"]:
                    if item.get("type") == "text":
                        text = item["text"]
                        try:
                            parsed = json.loads(text)
                            print(json.dumps(parsed, indent=2, ensure_ascii=False))
                        except (json.JSONDecodeError, TypeError):
                            print(text)
            else:
                print(json.dumps(content, indent=2, ensure_ascii=False))
    elif "error" in result:
        err = result["error"]
        print(f"错误 [{err.get('code', '?')}]: {err.get('message', '未知错误')}", file=sys.stderr)
        sys.exit(1)
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))


# ── CLI 入口 ──────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="猎聘 MCP CLI — 求职搜索、投递、简历管理",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--url", default=None, help="MCP 服务端 URL")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # setup
    sp_setup = subparsers.add_parser("setup", help="配置 token")
    sp_setup.set_defaults(func=cmd_setup)

    # list-tools
    sp_list = subparsers.add_parser("list-tools", help="列出可用工具")
    sp_list.add_argument("--json", action="store_true", help="JSON 输出")
    sp_list.set_defaults(func=cmd_list_tools)

    # search-job
    sp_search = subparsers.add_parser("search-job", help="搜索职位")
    sp_search.add_argument("--jobName", help="职位名称, 如 'AI产品经理'")
    sp_search.add_argument("--address", help="工作地点, 如 '上海'")
    sp_search.add_argument("--salary", help="薪资范围")
    sp_search.add_argument("--education", help="学历要求")
    sp_search.add_argument("--experience", help="工作经验")
    sp_search.add_argument("--companyType", help="公司类型")
    sp_search.add_argument("--companyName", help="公司名称")
    sp_search.add_argument("--json", action="store_true", help="JSON 输出")
    sp_search.set_defaults(func=cmd_search_job)

    # apply-job
    sp_apply = subparsers.add_parser("apply-job", help="投递职位")
    sp_apply.add_argument("--jobId", required=True, help="职位 ID")
    sp_apply.add_argument("--jobKind", required=True, help="职位类型")
    sp_apply.add_argument("--json", action="store_true", help="JSON 输出")
    sp_apply.set_defaults(func=cmd_apply_job)

    # my-resume
    sp_resume = subparsers.add_parser("my-resume", help="查看我的简历")
    sp_resume.add_argument("--json", action="store_true", help="JSON 输出")
    sp_resume.set_defaults(func=cmd_my_resume)

    # update-resume
    sp_update = subparsers.add_parser("update-resume", help="更新简历")
    sp_update.add_argument("--module", required=True, choices=["basic", "experience", "expectations", "self-assessment"], help="简历模块")
    sp_update.add_argument("--data", help="更新数据 (JSON 字符串)")
    sp_update.add_argument("--json", action="store_true", help="JSON 输出")
    sp_update.set_defaults(func=cmd_update_resume)

    # call (通用调用)
    sp_call = subparsers.add_parser("call", help="通用 MCP 工具调用")
    sp_call.add_argument("tool", help="工具名称")
    sp_call.add_argument("--arguments", "-a", help="参数 (JSON 字符串)")
    sp_call.add_argument("--json", action="store_true", help="JSON 输出")
    sp_call.set_defaults(func=cmd_call)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    args.func(args)


if __name__ == "__main__":
    main()
