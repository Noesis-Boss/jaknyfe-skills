import type { Context } from "hono";
import { Hono } from "hono";
import { Database } from "bun:sqlite";
import { randomUUID } from "crypto";

const app = new Hono();
const db = new Database(":memory:");

db.exec(`
  CREATE TABLE IF NOT EXISTS savings_goals (
    id TEXT PRIMARY KEY,
    userId TEXT NOT NULL,
    goalName TEXT NOT NULL,
    targetAmount REAL NOT NULL,
    currentAmount REAL DEFAULT 0,
    deadline TEXT NOT NULL,
    created_at TEXT NOT NULL
  );
`);

interface SavingsGoal {
  id: string;
  userId: string;
  goalName: string;
  targetAmount: number;
  currentAmount: number;
  deadline: string;
  created_at: string;
}

// GET /api/savings-goals - List all goals for a user
app.get("/api/savings-goals", (c: Context) => {
  const userId = c.req.query("userId") as string;
  if (!userId) {
    return c.json({ error: "userId required" }, 400);
  }
  const stmt = db.prepare("SELECT * FROM savings_goals WHERE userId = ? ORDER BY created_at DESC");
  const goals = stmt.all(userId) as SavingsGoal[];
  return c.json(goals);
});

// POST /api/savings-goals - Create a new savings goal
app.post("/api/savings-goals", async (c: Context) => {
  try {
    const body = await c.req.json();
    const { userId, goalName, targetAmount, currentAmount, deadline } = body;
    
    if (!userId || !goalName || !targetAmount || !deadline) {
      return c.json({ error: "Missing required fields: userId, goalName, targetAmount, deadline" }, 400);
    }
    
    if (typeof targetAmount !== "number" || targetAmount <= 0) {
      return c.json({ error: "targetAmount must be a positive number" }, 400);
    }
    
    const id = randomUUID();
    const created_at = new Date().toISOString();
    
    const stmt = db.prepare(
      "INSERT INTO savings_goals (id, userId, goalName, targetAmount, currentAmount, deadline, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)"
    );
    stmt.run(id, userId as string, goalName as string, targetAmount as number, currentAmount || 0, deadline as string, created_at);
    
    const goal: SavingsGoal = {
      id,
      userId,
      goalName,
      targetAmount,
      currentAmount: currentAmount || 0,
      deadline,
      created_at,
    };
    
    return c.json(goal, 201);
  } catch (err) {
    return c.json({ error: "Invalid request body" }, 400);
  }
});

// PATCH /api/savings-goals/:id - Update a savings goal
app.patch("/api/savings-goals/:id", async (c: Context) => {
  try {
    const id = c.req.param("id") as string;
    const body = await c.req.json();

    const getStmt = db.prepare("SELECT * FROM savings_goals WHERE id = ?");
    const goal = getStmt.get(id as string) as SavingsGoal | undefined;
    
    if (!goal) {
      return c.json({ error: "Goal not found" }, 404);
    }
    
    const updates: string[] = [];
    const values: any[] = [];
    
    if (body.goalName !== undefined) {
      updates.push("goalName = ?");
      values.push(body.goalName);
    }
    
    if (body.targetAmount !== undefined) {
      if (typeof body.targetAmount !== "number" || body.targetAmount <= 0) {
        return c.json({ error: "targetAmount must be a positive number" }, 400);
      }
      updates.push("targetAmount = ?");
      values.push(body.targetAmount);
    }
    
    if (body.currentAmount !== undefined) {
      if (typeof body.currentAmount !== "number" || body.currentAmount < 0) {
        return c.json({ error: "currentAmount must be non-negative" }, 400);
      }
      updates.push("currentAmount = ?");
      values.push(body.currentAmount);
    }
    
    if (body.deadline !== undefined) {
      updates.push("deadline = ?");
      values.push(body.deadline);
    }
    
    if (updates.length === 0) {
      return c.json(goal);
    }
    
    values.push(id as string);
    const updateStmt = db.prepare(`UPDATE savings_goals SET ${updates.join(", ")} WHERE id = ?`);
    updateStmt.run(values as any);

    const updatedGoal = getStmt.get(id as string);
    return c.json(updatedGoal);
  } catch (err) {
    return c.json({ error: "Invalid request body" }, 400);
  }
});

// DELETE /api/savings-goals/:id - Delete a savings goal
app.delete("/api/savings-goals/:id", (c: Context) => {
  const id = c.req.param("id") as string;

  const getStmt = db.prepare("SELECT * FROM savings_goals WHERE id = ?");
  const goal = getStmt.get(id as string);

  if (!goal) {
    return c.json({ error: "Goal not found" }, 404);
  }

  const deleteStmt = db.prepare("DELETE FROM savings_goals WHERE id = ?");
  deleteStmt.run(id as string);

  return c.json({ success: true, message: "Goal deleted" });
});

// Health check
app.get("/health", (c: Context) => {
  return c.json({ status: "ok" });
});

export default app;
