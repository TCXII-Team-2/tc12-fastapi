# Workflow Integration - Complete Setup

## Overview
The backend now automatically processes tickets through the agentic workflow when created via the frontend. This provides AI-powered analysis, validation, and response generation for every ticket.

## 🔄 Complete Workflow Flow

### 1. Frontend Creates Ticket
```
POST /api/v1/tickets/
{
  "sujet": "Billing issue",
  "description": "I was charged twice",
  "date_probleme": "2025-12-23T10:00:00"
}
```

### 2. Backend Processing (Automatic)
1. **Saves to Database** - Ticket stored with status `EN_TRAITEMENT`
2. **Sends to Workflow API** - Ticket analyzed by AI agents
3. **Stores AI Response** - Response saved in `responses` table
4. **Updates Status** - Ticket status updated based on workflow result:
   - `TRAITEE_AI` - AI provided a solution
   - `ESCALADE` - Needs human agent intervention
   - `EN_TRAITEMENT` - Needs clarification or is being processed

### 3. Workflow Returns
The workflow API provides:
- **Analysis** - Intent and category detection
- **Validation** - Checks if ticket is valid and in scope
- **RAG Retrieval** - Relevant knowledge base documents
- **Confidence** - Evaluation and escalation decision
- **Response** - Generated solution or message

## 📡 Available Endpoints

### Ticket Endpoints (with Workflow Integration)

#### Create Ticket (Auto-processes through workflow)
```http
POST /api/v1/tickets/
Authorization: Bearer <token>
Content-Type: application/json

{
  "sujet": "string",
  "description": "string",
  "date_probleme": "2025-12-23T10:00:00"
}

Response: TicketResponse with updated status
```

#### Get Ticket Details with Responses
```http
GET /api/v1/tickets/{ticket_id}/details
Authorization: Bearer <token>

Response: {
  "id": 1,
  "sujet": "...",
  "description": "...",
  "statut": "traitee_ai",
  "responses": [
    {
      "id": 1,
      "response_type": "AI",
      "response_text": "Here's how to fix...",
      "date_creation": "2025-12-23T10:01:00"
    }
  ]
}
```

#### Reprocess Ticket (Admin/Agent only)
```http
POST /api/v1/tickets/{ticket_id}/reprocess
Authorization: Bearer <token>

Response: Updated ticket with new AI response
```

### Direct Workflow Endpoints

#### Run Workflow Manually
```http
POST /api/v1/workflow/run
Authorization: Bearer <token>
Content-Type: application/json

{
  "id": "123",
  "subject": "Billing issue",
  "content": "I was charged twice",
  "created_at": "2025-12-23",
  "userPlan": "Pro"
}

Response: Complete workflow result with analysis, validation, RAG, confidence, and response
```

#### Bulk Q&A
```http
POST /api/v1/workflow/answer-questions
Authorization: Bearer <token>
Content-Type: application/json

{
  "Questions": [
    {"id": "q1", "query": "How do I reset password?"},
    {"id": "q2", "query": "What are your plans?"}
  ]
}

Response: {
  "Team": "TEAM 02",
  "Answers": [
    {"id": "q1", "answer": "To reset..."},
    {"id": "q2", "answer": "We offer..."}
  ]
}
```

#### Upload Knowledge Base Files
```http
POST /api/v1/workflow/knowledge/upload
Authorization: Bearer <token>
Content-Type: multipart/form-data

files: <file.md>
trigger_rebuild: true

Response: {
  "saved": ["C:\\...\\knowledge_base\\FAQ.md"],
  "rebuild_triggered": true
}
```

#### Rebuild Knowledge Base
```http
POST /api/v1/workflow/knowledge/rebuild
Authorization: Bearer <token>
?async_run=true

Response: {
  "status": "rebuild started"
}
```

## 🔧 Configuration

### 1. Set Workflow API URL
Update in `app/core/config.py` or set environment variable:
```python
WORKFLOW_API_URL="http://your-workflow-api-url:8000"
```

Or use environment variable:
```bash
export WORKFLOW_API_URL="http://localhost:8000"
```

### 2. Database Models
The integration uses:
- **Ticket** - Main ticket table with status tracking
- **Response** - Stores AI and agent responses
- **User** - Ticket ownership and authentication

### 3. Ticket Status Flow
```
EN_TRAITEMENT → (Workflow) → TRAITEE_AI / ESCALADE
     ↑                            ↓
     └────────(Agent Reply)───────┘
```

## 🚀 Usage Examples

### Frontend: Create Ticket
```javascript
const response = await fetch('/api/v1/tickets/', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    sujet: 'Cannot login',
    description: 'I forgot my password',
    date_probleme: new Date().toISOString()
  })
});

const ticket = await response.json();
// Ticket automatically processed by workflow
// Status updated based on AI analysis
```

### Frontend: Get Ticket with AI Response
```javascript
const response = await fetch(`/api/v1/tickets/${ticketId}/details`, {
  headers: { 'Authorization': `Bearer ${token}` }
});

const ticketDetails = await response.json();
// ticketDetails.responses contains AI-generated solutions
```

### Frontend: Display AI Response
```javascript
ticketDetails.responses.forEach(response => {
  if (response.response_type === 'AI') {
    console.log('AI Solution:', response.response_text);
  }
});
```

## 🛡️ Error Handling

If the workflow API fails:
- Ticket still saved to database
- Status remains `EN_TRAITEMENT`
- Error logged for admin review
- Ticket can be reprocessed later using `/reprocess` endpoint

## 📊 Monitoring

Check logs for workflow processing:
```
INFO: Ticket 123 processed by workflow with status traitee_ai
ERROR: Workflow processing failed for ticket 456: Connection timeout
```

## 🔐 Security

- All endpoints require authentication
- Knowledge base upload/rebuild restricted to admin/agent roles
- Ticket reprocessing restricted to admin/agent roles
- Users can only view their own tickets (unless admin/agent)

## 📝 Notes

- Workflow processing is asynchronous to avoid blocking ticket creation
- If workflow is unavailable, tickets are saved and can be processed later
- AI responses are stored with `response_type = "AI"` in the responses table
- Human agent responses can be added separately with `response_type = "agent"`

## 🔄 Complete Integration Checklist

- [x] Workflow schemas created
- [x] Workflow service with httpx client
- [x] Workflow endpoints (run, bulk Q&A, knowledge base)
- [x] Automatic ticket processing on creation
- [x] AI response storage in database
- [x] Status updates based on workflow results
- [x] Manual reprocessing endpoint
- [x] Detailed ticket endpoint with responses
- [x] Error handling and logging
- [x] Requirements updated with dependencies

## 🎯 Next Steps

1. Configure `WORKFLOW_API_URL` in your environment
2. Ensure workflow API is running and accessible
3. Test ticket creation from frontend
4. Monitor logs for successful processing
5. Verify AI responses are stored correctly
