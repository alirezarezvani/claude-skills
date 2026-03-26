# Attack Path Prerequisite Validation

Before asserting any lateral movement path from a compromised asset, validate the prerequisite chain. An attack path that omits required credentials or access vectors is an invalid finding and must not be presented to decision-makers.

## What a Compromised Perimeter Device Can DIRECTLY Achieve

A compromised network device (firewall, edge router, VPN gateway) enables the following without any additional credentials:

| Action | Rationale |
|---|---|
| Admin account creation on the device | Attacker has device admin access |
| Routing table manipulation | Native to device OS |
| Traffic interception of unencrypted sessions | Inline position on the network path |
| VPN gateway abuse to reach internal segments | If VPN is hosted on the device |
| DNS cache poisoning if device runs DNS | If DNS resolver is on the device |

## What Requires Additional Credentials — Validate Before Asserting

Each of the following attack paths has a hard prerequisite. Do not include it in the attack path output unless the prerequisite is confirmed or explicitly marked UNVERIFIED with the specific validation query.

| Secondary Target | Prerequisite Required | Validation Method |
|---|---|---|
| Cloud security group modification (AWS/Azure/GCP) | IAM credentials: access key + secret, or IAM role attached to a reachable EC2/VM instance, or IMDS v1 accessible from a host on the routed path | Check: is there a routable path from the compromised device to an EC2 instance with IMDS v1 enabled? Do CloudTrail logs show API calls from unexpected sources? |
| Kubernetes API server access | kubeconfig, service account token, or IMDS-derived token from a node on the network path | Check: is the K8s API server accessible from the firewall's network position? Are service account tokens mounted in pods on the reachable segment? |
| Okta admin modification | Okta administrator credentials or SAML assertion forgery (requires signing key) | Firewall position alone does not grant Okta admin access — this path is invalid without confirmed credential access |
| CI/CD pipeline secret access | Repository access token, GitHub PAT, or pipeline service account credentials | Firewall routing manipulation does not grant GitHub API access — check if secrets are stored on hosts reachable via the manipulated routing path |
| Database access | Database credentials + network path to database port | Firewall routing may enable network path; separate credential access is still required |

## Cloud Control Plane — Critical Constraint

A compromised on-premises or cloud-hosted firewall **cannot** modify cloud security groups, IAM policies, or VPC configurations without cloud API credentials. Routing table manipulation on the firewall affects network packet delivery — it does not grant cloud control plane API access. Both conditions must be true simultaneously for this attack path to be valid:

1. Attacker has established routing to a host with cloud API credentials.
2. Attacker has obtained or can obtain those cloud API credentials from the reachable host.

Until both are confirmed, the cloud control plane attack path must be marked: `PREREQUISITE_UNVERIFIED — requires IAM credential access confirmation`.
