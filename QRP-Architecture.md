# QRP Architecture: Implementation Roadmap

## 1. Deployment Strategy
The system is designed as a "Tenant-Based" deployment.

### Tenant Configuration File (`tenant_config.json`)
Each company is defined by a configuration file that points to their specific resources:
```json
{
  "tenant_id": "company_abc",
  "knowledge_base_id": "kb_v1_company_abc",
  "policy_file": "policies/company_abc_rules.yaml",
  "tool_set": {
    "crm": "salesforce",
    "communication": "slack",
    "erp": "sap"
  },
  "handoff_template": "standard_proposal_v2"
}
```

## 2. Technical Stack
- **Orchestration:** OpenClaw / Windmill (for data piping).
- **Intelligence:** Gemma4 / DeepSeek (via API/Local).
- **Memory:** Vector DB (Pinecone/Milvus/Qdrant) for the Context Layer.
- **Interface:** Telegram/Email for the "Application Engineer" to communicate with the customer.

## 3. Success Metrics (KPIs)
- **Lead Time Reduction:** Time from RFQ receipt to "Proposal Package" creation.
- **Completeness Rate:** Percentage of proposals that move to senior sales without requiring further technical clarification from the customer.
- **Accuracy:** Alignment between AI-generated technical brief and final engineering quote.
