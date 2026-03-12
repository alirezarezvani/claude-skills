// Reusable assertion helpers for skill quality evaluation
// Used by promptfoo configs via: type: javascript, value: file://eval/assertions/skill-quality.js

/**
 * Check that output demonstrates domain expertise (not generic advice).
 * Looks for specific terminology, frameworks, or tools mentioned.
 */
function hasDomainDepth(output, minTerms = 3) {
  // Count domain-specific patterns: frameworks, tools, methodologies, metrics
  const patterns = [
    /\b(RICE|MoSCoW|OKR|KPI|DORA|SLA|SLO|SLI)\b/gi,
    /\b(React|Next\.js|Tailwind|TypeScript|PostgreSQL|Redis|Lambda|S3)\b/gi,
    /\b(SEO|CRO|CTR|LTV|CAC|MRR|ARR|NPS|CSAT)\b/gi,
    /\b(OWASP|CVE|GDPR|SOC\s?2|ISO\s?27001|PCI)\b/gi,
    /\b(sprint|backlog|retrospective|standup|velocity)\b/gi,
  ];

  let termCount = 0;
  for (const pattern of patterns) {
    const matches = output.match(pattern);
    if (matches) termCount += new Set(matches.map(m => m.toLowerCase())).size;
  }

  return {
    pass: termCount >= minTerms,
    score: Math.min(1, termCount / (minTerms * 2)),
    reason: `Found ${termCount} domain-specific terms (minimum: ${minTerms})`,
  };
}

/**
 * Check that output is actionable (contains concrete next steps, not just analysis).
 */
function isActionable(output) {
  const actionPatterns = [
    /\b(step \d|first|second|third|next|then|finally)\b/gi,
    /\b(implement|create|build|configure|set up|install|deploy|run)\b/gi,
    /\b(action item|todo|checklist|recommendation)\b/gi,
    /```[\s\S]*?```/g, // code blocks indicate concrete output
  ];

  let score = 0;
  for (const pattern of actionPatterns) {
    if (pattern.test(output)) score += 0.25;
  }

  return {
    pass: score >= 0.5,
    score: Math.min(1, score),
    reason: `Actionability score: ${score}/1.0`,
  };
}

module.exports = { hasDomainDepth, isActionable };
