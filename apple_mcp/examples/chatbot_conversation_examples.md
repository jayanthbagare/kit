# Interactive Chatbot Conversation Examples

This document shows real conversation examples with the Apple Tonnage Prediction chatbot.

---

## Example 1: Successful Prediction

```
👤 User: /start

🤖 Bot: 🍎 *Apple Tonnage Prediction*

Let's get started! I'll need some information.

📍 Which city are you interested in?

Type one of: Riyadh, Jeddah, Dammam

---

👤 User: riyadh

🤖 Bot: Great! City: *Riyadh*

👥 Which customer?

Type one of: Lulu, Carrefour, Panda

---

👤 User: lulu

🤖 Bot: Perfect! Customer: *Lulu*

🍎 Which apple variety?

Type one of: fuji, gala, granny_smith

---

👤 User: fuji

🤖 Bot: Excellent! Variety: *fuji*

📅 Which year?

Type: 2024 or 2025

---

👤 User: 2024

🤖 Bot: Got it! Year: *2024*

📆 Which month?

Type one of: jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dec

---

👤 User: jan

🤖 Bot: Processing your prediction...

⏳ Please wait...

---

🤖 Bot: 🔴 *Tonnage Prediction Result*

📋 *Input Parameters:*
• City: Riyadh
• Customer: Lulu
• Variety: fuji
• Year: 2024
• Month: jan

📊 *Prediction:*
*74.23 tons*

📈 Demand Level: *High*

💡 Use /start for another prediction
```

---

## Example 2: Using Commands

### Help Command
```
👤 User: /help

🤖 Bot: 🤖 *Available Commands:*

/start - Start new prediction
/predict - Start new prediction
/valid - Show valid values
/cancel - Cancel current prediction
/help - Show this help
```

### Valid Values Command
```
👤 User: /valid

🤖 Bot: 📋 *Valid Values:*

*Cities:* Riyadh, Jeddah, Dammam
*Customers:* Lulu, Carrefour, Panda
*Varieties:* fuji, gala, granny_smith
*Months:* jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dec
*Years:* 2024, 2025

Use /start to begin a prediction.
```

### Cancel Command
```
👤 User: /start

🤖 Bot: 🍎 *Apple Tonnage Prediction*

Let's get started! I'll need some information.

📍 Which city are you interested in?

Type one of: Riyadh, Jeddah, Dammam

---

👤 User: riyadh

🤖 Bot: Great! City: *Riyadh*

👥 Which customer?

Type one of: Lulu, Carrefour, Panda

---

👤 User: /cancel

🤖 Bot: ❌ Prediction cancelled. Use /start to begin a new one.
```

---

## Example 3: Handling Input Errors

### Invalid City
```
👤 User: /start

🤖 Bot: 🍎 *Apple Tonnage Prediction*

Let's get started! I'll need some information.

📍 Which city are you interested in?

Type one of: Riyadh, Jeddah, Dammam

---

👤 User: dubai

🤖 Bot: ❌ Invalid city. Please choose: Riyadh, Jeddah, or Dammam

---

👤 User: riyadh

🤖 Bot: Great! City: *Riyadh*

👥 Which customer?

Type one of: Lulu, Carrefour, Panda
```

### Invalid Month
```
👤 User: january

🤖 Bot: ❌ Invalid month. Please type a valid month (jan, feb, mar, etc.)

---

👤 User: jan

🤖 Bot: Processing your prediction...

⏳ Please wait...
```

---

## Example 4: Medium Demand Prediction

```
👤 User: /start

🤖 Bot: [Conversation flow...]

---

👤 User: jan

🤖 Bot: 🟡 *Tonnage Prediction Result*

📋 *Input Parameters:*
• City: Dammam
• Customer: Carrefour
• Variety: gala
• Year: 2024
• Month: feb

📊 *Prediction:*
*55.40 tons*

📈 Demand Level: *Medium*

💡 Use /start for another prediction
```

---

## Example 5: Low Demand Prediction

```
👤 User: /start

🤖 Bot: [Conversation flow...]

---

👤 User: dec

🤖 Bot: 🟢 *Tonnage Prediction Result*

📋 *Input Parameters:*
• City: Dammam
• Customer: Panda
• Variety: granny_smith
• Year: 2024
• Month: dec

📊 *Prediction:*
*38.75 tons*

📈 Demand Level: *Low*

💡 Use /start for another prediction
```

---

## Example 6: Multiple Predictions in Sequence

```
👤 User: /start
🤖 Bot: [Completes first prediction for Riyadh/Lulu/Fuji]
🤖 Bot: *74.23 tons* (High Demand)

---

👤 User: /start
🤖 Bot: [Starts new conversation]

👤 User: jeddah
👤 User: carrefour
👤 User: gala
👤 User: 2024
👤 User: feb

🤖 Bot: 🔴 *Tonnage Prediction Result*

📋 *Input Parameters:*
• City: Jeddah
• Customer: Carrefour
• Variety: gala
• Year: 2024
• Month: feb

📊 *Prediction:*
*82.15 tons*

📈 Demand Level: *High*

💡 Use /start for another prediction
```

---

## Example 7: Model Not Trained Error

```
👤 User: /start

🤖 Bot: [Conversation flow...]

---

👤 User: jan

🤖 Bot: Processing your prediction...

⏳ Please wait...

---

🤖 Bot: ❌ *Prediction Error*

Model not trained. Please train the model first with CSV data.

Please make sure the model is trained. Use /start to try again.
```

**Solution:** Train the model first using the auto-training workflow or manually via HTTP endpoint.

---

## Example 8: Case Insensitivity

The bot accepts inputs in any case:

```
👤 User: RIYADH
🤖 Bot: ✅ Accepted (converted to "Riyadh")

👤 User: LuLu
🤖 Bot: ✅ Accepted (converted to "Lulu")

👤 User: FuJi
🤖 Bot: ✅ Accepted (converted to "fuji")
```

---

## Example 9: Unknown Command

```
👤 User: hello

🤖 Bot: ❓ I didn't understand that. Use /help to see available commands or /start to begin a prediction.

---

👤 User: what can you do?

🤖 Bot: ❓ I didn't understand that. Use /help to see available commands or /start to begin a prediction.
```

---

## Example 10: Quick Prediction (Minimal Interaction)

Advanced users can type responses quickly:

```
👤 User: /start
🤖 Bot: Which city?

👤 User: riyadh
🤖 Bot: Which customer?

👤 User: lulu
🤖 Bot: Which variety?

👤 User: fuji
🤖 Bot: Which year?

👤 User: 2024
🤖 Bot: Which month?

👤 User: jan
🤖 Bot: [Prediction result]
```

Total time: ~30 seconds for a complete prediction!

---

## Conversation State Management

### How It Works

The chatbot uses **workflow static data** to store conversation state:

```javascript
{
  "conv_123456789": {  // User ID
    "step": "ask_month",
    "data": {
      "city": "Riyadh",
      "customer_id": "Lulu",
      "apple_variety": "fuji",
      "year": 2024
    }
  }
}
```

### Features

1. **Per-User State**: Each user has their own conversation
2. **Persistent**: State survives workflow restarts
3. **Automatic Cleanup**: State cleared on completion or cancel
4. **Thread-Safe**: Multiple users can chat simultaneously

---

## Demand Level Indicators

The bot categorizes predictions into three levels:

| Demand Level | Tonnage Range | Emoji | Color |
|--------------|---------------|-------|-------|
| **High**     | > 70 tons     | 🔴    | Red   |
| **Medium**   | 50-70 tons    | 🟡    | Yellow|
| **Low**      | < 50 tons     | 🟢    | Green |

---

## Tips for Users

### Best Practices

1. **Use lowercase**: `riyadh` instead of `RIYADH` (both work, but lowercase is easier)
2. **Use short forms**: `jan` instead of `january`
3. **Type /cancel** if you make a mistake and want to start over
4. **Type /valid** to see all valid options before starting
5. **Keep bot token secure**: Never share your bot token publicly

### Common Mistakes

❌ **Typing full month names**: `january` → Use `jan`
❌ **Typing invalid years**: `2023` → Use `2024` or `2025`
❌ **Misspelled varieties**: `fugi` → Use `fuji`
❌ **Sending multiple values at once**: The bot processes one input at a time

---

## Advanced Features

### Multiple Users

The chatbot supports **unlimited concurrent users**. Each user's conversation is independent:

```
User A: [Currently at "ask_customer" step]
User B: [Currently at "ask_month" step]
User C: [Just completed prediction]
```

All three can chat with the bot simultaneously without interference!

### Conversation Timeout

Currently, the bot **does not timeout** conversations. If a user starts a prediction but doesn't finish, their state remains until:
- They complete the prediction
- They send `/cancel`
- They send `/start` (restarts the conversation)

**Future enhancement**: Add a timeout to auto-cancel conversations after 10 minutes of inactivity.

---

## Integration with Auto-Training Workflow

### Recommended Setup

Run **both workflows simultaneously**:

1. **Auto-Training Workflow**: Runs in background, monitors CSV, retrains model
2. **Chatbot Workflow**: Always active, ready to serve predictions

### User Experience

```
[CSV Updated] → [Auto-Training] → [Model Retrained] → [Notification Sent]
                                         ↓
                              [Chatbot now uses new model]
```

Users chatting with the bot will automatically get predictions from the latest trained model!

---

## Troubleshooting Conversations

### Issue: Bot doesn't respond
**Solution**: Check that the chatbot workflow is **activated** (toggle at bottom of n8n workflow)

### Issue: "Model not trained" error
**Solution**: Run the auto-training workflow or manually train via HTTP endpoint

### Issue: Bot forgets conversation mid-way
**Solution**: Check n8n workflow static data storage. May need to restart n8n.

### Issue: Multiple people getting mixed up conversations
**Solution**: Check that the conversation key uses `userId` not `chatId`

---

## Customization Ideas

### 1. Add Batch Predictions
Allow users to request multiple predictions at once

### 2. Add Export Feature
User types `/export` and gets a CSV file with multiple predictions

### 3. Add Visualization
Send charts/graphs showing demand trends

### 4. Add Notifications
User can subscribe to get alerts when model is retrained

### 5. Add Favorites
User can save common prediction queries

### 6. Multi-Language Support
Add Arabic language support for Saudi users

---

## Security & Privacy

### Data Storage

- Conversation state is stored in **n8n workflow static data** (in-memory)
- No conversation data is logged externally
- User IDs are used for state management but not stored permanently

### Best Practices

1. **Limit bot access**: Only share bot link with authorized users
2. **Use authentication**: Consider adding password/PIN for sensitive predictions
3. **Monitor usage**: Check n8n execution logs regularly
4. **Rate limiting**: Consider adding limits to prevent abuse

---

Happy chatting! 🤖🍎
