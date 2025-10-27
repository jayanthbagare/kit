# Telegram Message Templates

## 1. Success Message (Markdown Format)

```markdown
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

## 2. Failure Message

```markdown
⚠️ *Model Training Failed*

The apple tonnage prediction model failed to train with the latest CSV update.

Please check the CSV file format and server logs.

📅 10/27/2025, 5:30:45 PM
```

---

## 3. Enhanced Success Message with Multiple Predictions

```markdown
🍎 *Apple Tonnage Model Updated*

📊 *Training Results:*
- Model Type: random_forest
- Training Samples: 1800
- Mean Absolute Error: 12.34
- R² Score: 0.8567

🎯 *Key Predictions for January 2024:*

*Riyadh*
├─ Lulu/Fuji: 74.23 tons
├─ Carrefour/Gala: 68.45 tons
└─ Panda/Granny Smith: 52.10 tons

*Jeddah*
├─ Lulu/Fuji: 82.15 tons
├─ Carrefour/Gala: 75.30 tons
└─ Panda/Granny Smith: 61.20 tons

*Dammam*
├─ Lulu/Fuji: 55.40 tons
├─ Carrefour/Gala: 48.90 tons
└─ Panda/Granny Smith: 38.75 tons

⚠️ Please review the new predictions and adjust purchasing plans accordingly.

📅 Updated: 10/27/2025, 5:30:45 PM
```

---

## 4. Message with Model Comparison

```markdown
🍎 *Apple Tonnage Model Updated*

📊 *Training Results:*
- Model Type: random_forest
- Training Samples: 1800
- Mean Absolute Error: 12.34 (↓ 2.1 from previous)
- R² Score: 0.8567 (↑ 0.05 from previous)

📈 *Model Improvement:*
The new model shows 15% better accuracy!

🎯 *Sample Prediction (Riyadh/Lulu/Fuji/Jan):*
- New Prediction: *74.23 tons*
- Previous Prediction: 71.50 tons
- Change: +2.73 tons (+3.8%)

⚠️ Please review the new predictions and adjust purchasing plans accordingly.

📅 Updated: 10/27/2025, 5:30:45 PM
```

---

## 5. Actionable Message with Recommendations

```markdown
🍎 *Apple Tonnage Model Updated*

📊 *Training Results:*
- Model: Random Forest
- Samples: 1800
- Accuracy: R² = 0.8567

🎯 *January 2024 Predictions:*

🔴 *High Demand (>70 tons):*
- Riyadh/Lulu/Fuji: 74.23 tons
- Jeddah/Lulu/Fuji: 82.15 tons

🟡 *Medium Demand (50-70 tons):*
- Riyadh/Carrefour/Gala: 68.45 tons
- Dammam/Lulu/Fuji: 55.40 tons

🟢 *Low Demand (<50 tons):*
- Dammam/Panda/Granny Smith: 38.75 tons

📋 *Action Items:*
✅ Increase Fuji inventory for Riyadh and Jeddah
✅ Monitor Gala demand in Carrefour stores
✅ Consider promotional pricing for Granny Smith

📅 Updated: 10/27/2025, 5:30:45 PM
```

---

## 6. Weekly Summary Message

```markdown
📊 *Weekly Apple Tonnage Summary*

Period: Oct 20 - Oct 27, 2025

📈 *Model Updates:*
- Total Retrains: 5
- Average R² Score: 0.8542
- Best MAE: 11.87

🎯 *Top 5 Highest Predictions:*
1. Jeddah/Lulu/Fuji (Feb): 85.30 tons
2. Riyadh/Lulu/Fuji (Jan): 74.23 tons
3. Jeddah/Carrefour/Gala (Feb): 76.10 tons
4. Riyadh/Carrefour/Gala (Jan): 68.45 tons
5. Dammam/Lulu/Fuji (Mar): 62.15 tons

📉 *Trends:*
- Fuji variety showing strongest demand
- Jeddah market growing 8% vs last week
- Granny Smith demand stable

💡 *Recommendation:*
Focus procurement on Fuji variety for Jeddah and Riyadh markets.

📅 Generated: 10/27/2025, 5:30:45 PM
```

---

## Usage in n8n Code Node

### Basic Message (from workflow)
```javascript
const trainingData = $input.first().json;
const predictionData = $input.last().json;

const message = `🍎 *Apple Tonnage Model Updated*\n\n` +
  `📊 *Training Results:*\n` +
  `- Model Type: ${trainingData.model_type}\n` +
  `- Training Samples: ${trainingData.training_samples}\n` +
  `- Mean Absolute Error: ${parseFloat(trainingData.mae).toFixed(2)}\n` +
  `- R² Score: ${parseFloat(trainingData.r2_score).toFixed(4)}\n\n` +
  `🎯 *Sample Prediction:*\n` +
  `- City: ${predictionData.inputs.city}\n` +
  `- Customer: ${predictionData.inputs.customer_id}\n` +
  `- Variety: ${predictionData.inputs.apple_variety}\n` +
  `- Month: ${predictionData.inputs.month}\n` +
  `- Predicted Tonnage: *${parseFloat(predictionData.prediction).toFixed(2)} tons*\n\n` +
  `⚠️ Please review the new predictions and adjust purchasing plans accordingly.\n\n` +
  `📅 Updated: ${new Date().toLocaleString()}`;

return { message };
```

### Enhanced Message with Thresholds
```javascript
const trainingData = $input.first().json;
const predictionData = $input.last().json;
const prediction = parseFloat(predictionData.prediction);

// Determine urgency
let urgencyEmoji = '🟢';
let urgencyText = 'Low Demand';
if (prediction > 70) {
  urgencyEmoji = '🔴';
  urgencyText = 'High Demand';
} else if (prediction > 50) {
  urgencyEmoji = '🟡';
  urgencyText = 'Medium Demand';
}

const message = `${urgencyEmoji} *Apple Tonnage Alert*\n\n` +
  `📊 *Model Updated*\n` +
  `- Accuracy: R² = ${parseFloat(trainingData.r2_score).toFixed(4)}\n` +
  `- Samples: ${trainingData.training_samples}\n\n` +
  `🎯 *Prediction: ${urgencyText}*\n` +
  `- Location: ${predictionData.inputs.city}\n` +
  `- Customer: ${predictionData.inputs.customer_id}\n` +
  `- Product: ${predictionData.inputs.apple_variety}\n` +
  `- Expected: *${prediction.toFixed(2)} tons*\n\n` +
  `⚠️ Action: ${prediction > 70 ? 'Increase inventory immediately!' : 'Monitor demand trends.'}\n\n` +
  `📅 ${new Date().toLocaleString()}`;

return { message };
```

---

## Customization Tips

1. **Add Emojis**: Use emojis to make messages more visual and engaging
2. **Markdown Formatting**: Use `*bold*`, `_italic_`, `` `code` `` for emphasis
3. **Thresholds**: Add logic to change message tone based on prediction values
4. **Multiple Languages**: Add translation support for international teams
5. **Charts**: Consider sending charts/graphs as images (requires additional nodes)
6. **Links**: Add links to dashboards or detailed reports
7. **Mentions**: Use `@username` to mention specific team members

---

## Testing Messages

### Quick Test with curl
```bash
# Replace YOUR_BOT_TOKEN and YOUR_CHAT_ID
curl -X POST "https://api.telegram.org/botYOUR_BOT_TOKEN/sendMessage" \
  -H "Content-Type: application/json" \
  -d '{
    "chat_id": "YOUR_CHAT_ID",
    "text": "🍎 *Test Message*\n\nThis is a test from the Apple Tonnage system.",
    "parse_mode": "Markdown"
  }'
```

---

## Best Practices

1. **Keep it concise**: Busy managers prefer short, actionable messages
2. **Highlight key numbers**: Use bold/emphasis for important predictions
3. **Add context**: Include date, model accuracy, sample size
4. **Call to action**: Tell the manager what to do with the information
5. **Use emojis wisely**: Enhance readability but don't overdo it
6. **Test formatting**: Always test Markdown rendering in Telegram first
