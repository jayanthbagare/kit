# n8n Automation Setup Guide
## Auto-Train Model & Interactive Chatbot

This guide will help you set up two n8n workflows:

### Workflow 1: Auto-Training & Alerts
1. Monitors your CSV file for changes
2. Automatically retrains the model when CSV is updated
3. Gets a sample prediction
4. Sends a Telegram message to the purchasing manager

### Workflow 2: Interactive Chatbot
1. Chat with the bot on Telegram to get predictions
2. Bot asks for city, customer, variety, year, and month
3. Returns prediction with demand level analysis
4. Supports commands like /start, /help, /valid, /cancel

---

## Prerequisites

### 1. Install n8n
```bash
# Using npm (recommended)
npm install -g n8n

# Or using Docker
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n
```

### 2. Start the MCP HTTP Server
```bash
cd /Users/I028960/Projects/apple_mcp
python3 http_mcp_wrapper.py
```

The server should be running on `http://localhost:8000`

### 3. Set up Telegram Bot

#### Step 3.1: Create a Telegram Bot
1. Open Telegram and search for `@BotFather`
2. Send `/newbot` command
3. Follow the prompts to name your bot (e.g., "Apple Tonnage Alert Bot")
4. BotFather will give you an **API Token** - save this!

Example:
```
Use this token to access the HTTP API:
1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
```

#### Step 3.2: Get Your Chat ID
1. Send a message to your bot (e.g., "Hello")
2. Visit this URL in your browser (replace TOKEN with your bot token):
   ```
   https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates
   ```
3. Look for `"chat":{"id":123456789}` in the response
4. Save this **Chat ID**

Example response:
```json
{
  "ok": true,
  "result": [{
    "message": {
      "chat": {
        "id": 123456789,
        "first_name": "Your Name"
      }
    }
  }]
}
```

---

## n8n Workflow Setup

### Step 1: Start n8n
```bash
n8n start
```

Access n8n at: `http://localhost:5678`

### Step 2: Configure Telegram Credentials in n8n

1. Go to **Settings** → **Credentials** → **Add Credential**
2. Search for "Telegram"
3. Select "Telegram API"
4. Enter your **Bot Token** from BotFather
5. Name it "Telegram Purchasing Manager Bot"
6. Click **Save**

### Step 3: Import the Workflows

#### Option A: Auto-Training Workflow
1. In n8n, click **Workflows** → **Import from File**
2. Select the file: `examples/n8n_workflow_auto_training.json`
3. The workflow will be imported

#### Option B: Interactive Chatbot Workflow
1. In n8n, click **Workflows** → **Import from File**
2. Select the file: `examples/n8n_workflow_interactive_chatbot.json`
3. The workflow will be imported

**Note:** You can run both workflows simultaneously!

### Step 4: Configure the Workflows

#### For Auto-Training Workflow:

**A. Watch CSV File Node**
- Update the `path` parameter to your actual CSV file location:
  ```
  /Users/I028960/Projects/apple_mcp/examples/sample_data.csv
  ```
- Or use your production CSV path

**B. Get Sample Prediction Node**
Customize the prediction inputs (optional):
- Change `city`, `customer_id`, `apple_variety`, `year`, `month` to values relevant to your business
- This prediction will be shown in the Telegram message

**C. Send Telegram Message Node**
1. Click on the node
2. In **Credentials**, select "Telegram Purchasing Manager Bot"
3. In **Chat ID**, enter your chat ID (e.g., `123456789`)

**D. Send Failure Alert Node**
1. Click on the node
2. In **Credentials**, select "Telegram Purchasing Manager Bot"
3. In **Chat ID**, enter your chat ID

#### For Interactive Chatbot Workflow:

**A. Telegram Trigger Node**
1. Click on the node
2. In **Credentials**, select "Telegram Purchasing Manager Bot"
3. Save the node

**B. Send Response Node**
1. Click on the node
2. In **Credentials**, select "Telegram Purchasing Manager Bot"

**C. Send Prediction Node**
1. Click on the node
2. In **Credentials**, select "Telegram Purchasing Manager Bot"

That's it! The chatbot workflow uses conversation state management and doesn't need Chat IDs configured.

### Step 5: Test the Workflows

#### Testing Auto-Training Workflow:
1. Click **Execute Workflow** button in n8n
2. Modify your CSV file (add a row or change a value)
3. Wait for the trigger to fire (may take up to 1 minute)
4. Check your Telegram for the message!

#### Testing Interactive Chatbot:
1. **Activate** the workflow in n8n (toggle switch at bottom)
2. Open Telegram and send `/start` to your bot
3. Follow the interactive conversation
4. The bot will ask for: city → customer → variety → year → month
5. Get your prediction!

**Example conversation:**
```
You: /start
Bot: Which city? (Riyadh, Jeddah, Dammam)
You: riyadh
Bot: Which customer? (Lulu, Carrefour, Panda)
You: lulu
Bot: Which variety? (fuji, gala, granny_smith)
You: fuji
Bot: Which year? (2024, 2025)
You: 2024
Bot: Which month? (jan, feb, mar...)
You: jan
Bot: [Returns prediction with demand level]
```

---

## Workflow Details

### Auto-Training Workflow Nodes

1. **Watch CSV File** (File Trigger)
   - Monitors the CSV file every minute
   - Triggers when the file is modified
   - Passes the file path to the next node

2. **Train Model** (HTTP Request)
   - Sends POST request to `http://localhost:8000/train`
   - Includes CSV path and model type
   - Returns training metrics

3. **Check Training Success** (IF Node)
   - Checks if training status is "success"
   - Routes to success or failure path

4. **Extract Training Metrics** (Set Node)
   - Extracts relevant training data
   - Prepares data for the message

5. **Get Sample Prediction** (HTTP Request)
   - Makes a prediction with sample inputs
   - Shows what the model predicts

6. **Format Telegram Message** (Code Node)
   - Creates a formatted Markdown message
   - Includes training metrics and prediction

7. **Send Telegram Message** (Telegram Node)
   - Sends the alert to the purchasing manager
   - Uses Markdown formatting

8. **Send Failure Alert** (Telegram Node)
   - Sends an error message if training fails

### Interactive Chatbot Workflow Nodes

1. **Telegram Trigger** (Telegram Trigger)
   - Listens for all messages sent to the bot
   - Triggers the workflow on every message
   - Passes message data to the next node

2. **Process Conversation** (Code Node)
   - Manages conversation state using workflow static data
   - Handles commands: /start, /help, /valid, /cancel
   - Validates user inputs at each step
   - Guides user through: city → customer → variety → year → month
   - Stores conversation progress per user ID

3. **Check If Ready to Predict** (IF Node)
   - Checks if all inputs are collected (step = 'complete')
   - Routes to prediction or back to conversation

4. **Send Response** (Telegram Node)
   - Sends conversational prompts to user
   - Handles validation errors
   - Provides help and command responses

5. **Get Prediction** (HTTP Request)
   - Calls `http://localhost:8000/predict` with collected inputs
   - Returns prediction from MCP server

6. **Format Prediction Response** (Code Node)
   - Formats final prediction message
   - Adds demand level analysis (High/Medium/Low)
   - Creates user-friendly Markdown message

7. **Send Prediction** (Telegram Node)
   - Sends final prediction result to user
   - Includes emoji indicators for demand levels

---

## Customization Options

### 1. Change Monitoring Frequency
In the "Watch CSV File" node:
- **Every Minute**: Default (good for testing)
- **Every 5 Minutes**: `*/5 * * * *`
- **Every Hour**: `0 * * * *`
- **Every Day at 9 AM**: `0 9 * * *`

### 2. Multiple Predictions
Modify the "Get Sample Prediction" node to use the `/batch-predict` endpoint:

```json
{
  "predictions": [
    {"city": "Riyadh", "customer_id": "Lulu", "apple_variety": "fuji", "year": 2024, "month": "jan"},
    {"city": "Jeddah", "customer_id": "Carrefour", "apple_variety": "gala", "year": 2024, "month": "feb"}
  ]
}
```

### 3. Add More Recipients
Duplicate the "Send Telegram Message" node and add different Chat IDs for multiple managers.

### 4. Add Email Notifications
Add an **Email** node after the message formatting to send emails too.

### 5. Store Predictions in Database
Add a **Database** node (PostgreSQL, MySQL, etc.) to log all predictions for historical tracking.

---

## Example Telegram Message

When everything is set up, your purchasing manager will receive a message like:

```
🍎 *Apple Tonnage Model Updated*

📊 *Training Results:*
- Model Type: random_forest
- Training Samples: 1800
- Mean Absolute Error: 12.34
- R² Score: 0.8567

🎯 *Sample Prediction:*
- City: Riyadh
- Customer: Lulu
- Variety: fuji
- Month: jan
- Predicted Tonnage: *74.23 tons*

⚠️ Please review the new predictions and adjust purchasing plans accordingly.

📅 Updated: 10/27/2025, 5:30:45 PM
```

---

## Troubleshooting

### Issue: Workflow doesn't trigger
- **Check**: Is the CSV file path correct?
- **Check**: Is the file actually being modified?
- **Try**: Manually execute the workflow to test

### Issue: Training fails
- **Check**: Is `http_mcp_wrapper.py` running?
- **Check**: Can you access `http://localhost:8000/health`?
- **Check**: Is the CSV format correct?

### Issue: Telegram message not sent
- **Check**: Is the Bot Token correct?
- **Check**: Is the Chat ID correct?
- **Check**: Did you send a message to the bot first?
- **Try**: Test with the Telegram API URL directly

### Issue: "Connection refused" error
- **Check**: MCP server is running on port 8000
- **Try**: `curl http://localhost:8000/health`

### Check Server Health
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "model_trained": false
}
```

---

## Production Deployment

### 1. Run MCP Server as a Service

Create a systemd service file (Linux):
```bash
sudo nano /etc/systemd/system/apple-mcp.service
```

Content:
```ini
[Unit]
Description=Apple Tonnage MCP Server
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/Users/I028960/Projects/apple_mcp
ExecStart=/usr/bin/python3 http_mcp_wrapper.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable apple-mcp
sudo systemctl start apple-mcp
```

### 2. Run n8n as a Service

```bash
sudo npm install -g pm2
pm2 start n8n
pm2 save
pm2 startup
```

### 3. Use Environment Variables

Store sensitive data in environment variables:
- Telegram Bot Token
- Chat IDs
- File paths

---

## Advanced Features

### 1. Add Validation Checks
Add nodes to validate CSV data quality before training.

### 2. Compare with Previous Model
Store previous predictions and show improvements/changes.

### 3. Alert Thresholds
Only send Telegram alerts if the prediction changes by more than X%.

### 4. Schedule Regular Reports
Create a separate workflow that sends daily/weekly summary reports.

---

## Support

If you encounter issues:
1. Check n8n logs: In n8n, go to **Executions** to see detailed logs
2. Check MCP server logs: Terminal where `http_mcp_wrapper.py` is running
3. Test endpoints manually with `curl` or Postman

---

## Next Steps

1. ✅ Set up Telegram bot
2. ✅ Import workflow into n8n
3. ✅ Configure credentials and Chat ID
4. ✅ Update CSV file path
5. ✅ Test the workflow
6. ✅ Deploy to production
7. ✅ Monitor and refine

Happy automating! 🚀
