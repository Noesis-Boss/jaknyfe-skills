# Savings Goals API

REST API for managing user savings goals.

## Schema

```
{
  "id": "uuid",
  "userId": "string",
  "goalName": "string",
  "targetAmount": "number",
  "currentAmount": "number",
  "deadline": "string (ISO date)",
  "created_at": "string (ISO timestamp)"
}
```

## Endpoints

### GET /api/savings-goals
List all savings goals for a user.

**Query Parameters:**
- `userId` (required): The user ID

**Response:** Array of savings goals

```bash
curl "https://jaknyfe.zo.space/api/savings-goals?userId=user123"
```

### POST /api/savings-goals
Create a new savings goal.

**Request Body:**
```json
{
  "userId": "user123",
  "goalName": "Vacation Fund",
  "targetAmount": 5000,
  "currentAmount": 1200,
  "deadline": "2025-12-31"
}
```

**Response:** 201 Created with goal object

```bash
curl -X POST https://jaknyfe.zo.space/api/savings-goals \
  -H "Content-Type: application/json" \
  -d '{
    "userId": "user123",
    "goalName": "Vacation Fund",
    "targetAmount": 5000,
    "deadline": "2025-12-31"
  }'
```

### PATCH /api/savings-goals/:id
Update a savings goal.

**Request Body:** Any fields to update (goalName, targetAmount, currentAmount, deadline)

**Response:** Updated goal object

```bash
curl -X PATCH https://jaknyfe.zo.space/api/savings-goals/goal-id \
  -H "Content-Type: application/json" \
  -d '{"currentAmount": 2500}'
```

### DELETE /api/savings-goals/:id
Delete a savings goal.

**Response:** `{ "success": true }`

```bash
curl -X DELETE https://jaknyfe.zo.space/api/savings-goals/goal-id
```

## Error Handling

All errors return appropriate HTTP status codes and error messages:

- `400 Bad Request`: Missing required fields or invalid input
- `404 Not Found`: Goal not found
- `500 Internal Server Error`: Server error

Example error response:
```json
{
  "error": "Missing required fields: userId, goalName, targetAmount, deadline"
}
```

## Notes

- Currently uses in-memory SQLite database (data is lost on restart)
- For production, migrate to persistent SQLite file or PostgreSQL
- Implement user authentication/authorization as needed
