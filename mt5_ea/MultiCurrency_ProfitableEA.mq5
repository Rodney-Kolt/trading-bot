//+------------------------------------------------------------------+
//| MultiCurrency_ProfitableEA.mq5                                  |
//| Multi-Currency Profitable Trading EA - Small Wins Focus        |
//| Monitors multiple currency pairs simultaneously                  |
//+------------------------------------------------------------------+

#property copyright "Multi-Currency Profitable Trading System"
#property version   "1.00"

// Input Parameters - PROFITABLE DEFAULTS
input string    WebhookURL = "https://trading-bot-production-c863.up.railway.app/webhook";
input int       FastEMA = 9;
input int       SlowEMA = 21;
input int       TrendEMA = 200;
input int       RSIPeriod = 14;
input double    RiskPercent = 0.5;         // Small wins: 0.5% risk per trade
input double    StopLossPercent = 0.5;     // Tight stops: 0.5%
input double    TakeProfitPercent = 0.6;   // 1:1.2 risk/reward ratio
input bool      SendWebhooks = true;
input bool      ExecuteOnMT5 = false;      // Start in signal-only mode

// Currency pairs to monitor
string symbols[] = {"EURUSD", "GBPUSD", "USDJPY", "AUDUSD"};
int symbolCount = 4;

// Indicator handles for each symbol
struct SymbolData {
    int fastEMAHandle;
    int slowEMAHandle;
    int trendEMAHandle;
    int rsiHandle;
    datetime lastSignalTime;
    bool inPosition;
    double entryPrice;
};

SymbolData symbolData[];

//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit()
{
    Print("🚀 Multi-Currency Profitable EA Started - Small Wins Focus");
    Print("💰 Monitoring ", symbolCount, " currency pairs");
    
    // Resize array to match symbol count
    ArrayResize(symbolData, symbolCount);
    
    // Initialize indicators for each symbol
    for(int i = 0; i < symbolCount; i++)
    {
        string symbol = symbols[i];
        Print("📊 Initializing indicators for ", symbol);
        
        symbolData[i].fastEMAHandle = iMA(symbol, PERIOD_M15, FastEMA, 0, MODE_EMA, PRICE_CLOSE);
        symbolData[i].slowEMAHandle = iMA(symbol, PERIOD_M15, SlowEMA, 0, MODE_EMA, PRICE_CLOSE);
        symbolData[i].trendEMAHandle = iMA(symbol, PERIOD_M15, TrendEMA, 0, MODE_EMA, PRICE_CLOSE);
        symbolData[i].rsiHandle = iRSI(symbol, PERIOD_M15, RSIPeriod, PRICE_CLOSE);
        
        if(symbolData[i].fastEMAHandle == INVALID_HANDLE || 
           symbolData[i].slowEMAHandle == INVALID_HANDLE || 
           symbolData[i].trendEMAHandle == INVALID_HANDLE || 
           symbolData[i].rsiHandle == INVALID_HANDLE)
        {
            Print("❌ Failed to initialize indicators for ", symbol);
            return INIT_FAILED;
        }
        
        symbolData[i].lastSignalTime = 0;
        symbolData[i].inPosition = false;
        symbolData[i].entryPrice = 0;
        
        Print("✅ ", symbol, " indicators initialized successfully");
    }
    
    Print("📡 Webhook URL: ", WebhookURL);
    Print("💰 Risk per trade: ", RiskPercent, "%");
    Print("🛡️ Stop Loss: ", StopLossPercent, "%");
    Print("🎯 Take Profit: ", TakeProfitPercent, "%");
    Print("🌍 Multi-Currency EA ready!");
    
    return INIT_SUCCEEDED;
}

//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
{
    // Check for new bar on each symbol
    static datetime lastBarTimes[];
    ArrayResize(lastBarTimes, symbolCount);
    
    for(int i = 0; i < symbolCount; i++)
    {
        string symbol = symbols[i];
        datetime currentBarTime = iTime(symbol, PERIOD_M15, 0);
        
        if(currentBarTime == lastBarTimes[i])
            continue;
        
        lastBarTimes[i] = currentBarTime;
        
        // Check for signals on this symbol
        CheckForSignals(i, symbol);
        
        // Manage existing positions
        ManagePositions(i, symbol);
    }
}

//+------------------------------------------------------------------+
//| Check for trading signals on specific symbol                    |
//+------------------------------------------------------------------+
void CheckForSignals(int index, string symbol)
{
    double currentPrice = SymbolInfoDouble(symbol, SYMBOL_BID);
    
    // Prevent multiple signals in short time
    if(TimeCurrent() - symbolData[index].lastSignalTime < 300) // 5 minutes cooldown
        return;
    
    // Get indicator values
    double fastEMA[], slowEMA[], trendEMA[], rsi[];
    
    ArraySetAsSeries(fastEMA, true);
    ArraySetAsSeries(slowEMA, true);
    ArraySetAsSeries(trendEMA, true);
    ArraySetAsSeries(rsi, true);
    
    if(CopyBuffer(symbolData[index].fastEMAHandle, 0, 0, 3, fastEMA) < 3 ||
       CopyBuffer(symbolData[index].slowEMAHandle, 0, 0, 3, slowEMA) < 3 ||
       CopyBuffer(symbolData[index].trendEMAHandle, 0, 0, 3, trendEMA) < 3 ||
       CopyBuffer(symbolData[index].rsiHandle, 0, 0, 3, rsi) < 3)
    {
        Print("❌ Failed to copy indicator values for ", symbol);
        return;
    }
    
    // BUY Signal Conditions
    bool buySignal = false;
    if(!symbolData[index].inPosition && 
       currentPrice > trendEMA[0] &&           // Above trend EMA
       fastEMA[1] <= slowEMA[1] &&             // Previous: Fast EMA below Slow EMA
       fastEMA[0] > slowEMA[0] &&              // Current: Fast EMA above Slow EMA (crossover)
       rsi[0] < 70)                            // RSI not overbought
    {
        buySignal = true;
    }
    
    // SELL Signal Conditions  
    bool sellSignal = false;
    if(symbolData[index].inPosition &&
       (currentPrice <= symbolData[index].entryPrice * (1 - StopLossPercent/100) ||     // Stop loss hit
        currentPrice >= symbolData[index].entryPrice * (1 + TakeProfitPercent/100) ||   // Take profit hit
        (fastEMA[1] >= slowEMA[1] && fastEMA[0] < slowEMA[0])))                        // EMA crossunder
    {
        sellSignal = true;
    }
    
    // Execute signals
    if(buySignal)
    {
        ExecuteBuySignal(index, symbol, currentPrice);
    }
    else if(sellSignal)
    {
        ExecuteSellSignal(index, symbol, currentPrice);
    }
}

//+------------------------------------------------------------------+
//| Execute BUY signal                                               |
//+------------------------------------------------------------------+
void ExecuteBuySignal(int index, string symbol, double price)
{
    Print("🟢 ", symbol, " BUY Signal Generated at ", price);
    
    // Send webhook to Python bot
    if(SendWebhooks)
    {
        SendWebhookSignal("BUY", symbol, price);
    }
    
    // Execute on MT5 if enabled
    if(ExecuteOnMT5)
    {
        ExecuteMT5Buy(index, symbol, price);
    }
    
    symbolData[index].lastSignalTime = TimeCurrent();
}

//+------------------------------------------------------------------+
//| Execute SELL signal                                              |
//+------------------------------------------------------------------+
void ExecuteSellSignal(int index, string symbol, double price)
{
    Print("🔴 ", symbol, " SELL Signal Generated at ", price);
    
    // Send webhook to Python bot
    if(SendWebhooks)
    {
        SendWebhookSignal("SELL", symbol, price);
    }
    
    // Execute on MT5 if enabled
    if(ExecuteOnMT5)
    {
        ExecuteMT5Sell(index, symbol, price);
    }
    
    symbolData[index].lastSignalTime = TimeCurrent();
}

//+------------------------------------------------------------------+
//| Send webhook signal to Python bot                               |
//+------------------------------------------------------------------+
void SendWebhookSignal(string action, string symbol, double price)
{
    string headers = "Content-Type: application/json\r\n";
    string data = StringFormat(
        "{\"action\":\"%s\",\"symbol\":\"%s\",\"price\":\"%.5f\",\"strategy\":\"MultiCurrency_EMA_RSI\",\"timeframe\":\"15m\"}",
        action, symbol, price
    );
    
    char post[], result[];
    StringToCharArray(data, post, 0, StringLen(data));
    
    int res = WebRequest("POST", WebhookURL, headers, 5000, post, result, headers);
    
    if(res == 200)
    {
        Print("✅ Webhook sent successfully: ", symbol, " ", action, " at ", price);
    }
    else
    {
        Print("❌ Webhook failed for ", symbol, ". Code: ", res);
    }
}

//+------------------------------------------------------------------+
//| Execute BUY on MT5                                               |
//+------------------------------------------------------------------+
void ExecuteMT5Buy(int index, string symbol, double price)
{
    if(symbolData[index].inPosition)
        return;
    
    double lotSize = 0.01; // Fixed small lot size for safety
    double sl = price * (1 - StopLossPercent/100);
    double tp = price * (1 + TakeProfitPercent/100);
    
    MqlTradeRequest request;
    MqlTradeResult result;
    
    ZeroMemory(request);
    request.action = TRADE_ACTION_DEAL;
    request.symbol = symbol;
    request.volume = lotSize;
    request.type = ORDER_TYPE_BUY;
    request.price = SymbolInfoDouble(symbol, SYMBOL_ASK);
    request.sl = sl;
    request.tp = tp;
    request.deviation = 10;
    request.magic = 123456;
    request.comment = "Multi-Currency EA Buy";
    
    if(OrderSend(request, result))
    {
        Print("✅ ", symbol, " BUY executed: ", result.price, " SL:", sl, " TP:", tp);
        symbolData[index].inPosition = true;
        symbolData[index].entryPrice = result.price;
    }
    else
    {
        Print("❌ ", symbol, " BUY failed: ", result.retcode);
    }
}

//+------------------------------------------------------------------+
//| Execute SELL on MT5                                              |
//+------------------------------------------------------------------+
void ExecuteMT5Sell(int index, string symbol, double price)
{
    if(!symbolData[index].inPosition)
        return;
    
    // Close position for this symbol
    for(int i = PositionsTotal()-1; i >= 0; i--)
    {
        if(PositionGetSymbol(i) == symbol)
        {
            MqlTradeRequest request;
            MqlTradeResult result;
            
            ZeroMemory(request);
            request.action = TRADE_ACTION_DEAL;
            request.symbol = symbol;
            request.volume = PositionGetDouble(POSITION_VOLUME);
            request.type = ORDER_TYPE_SELL;
            request.price = SymbolInfoDouble(symbol, SYMBOL_BID);
            request.position = PositionGetInteger(POSITION_TICKET);
            request.magic = 123456;
            request.comment = "Multi-Currency EA Sell";
            
            if(OrderSend(request, result))
            {
                double pnl = result.price - symbolData[index].entryPrice;
                Print("✅ ", symbol, " SELL executed: ", result.price, " P&L: ", pnl);
                symbolData[index].inPosition = false;
                symbolData[index].entryPrice = 0;
            }
            break;
        }
    }
}

//+------------------------------------------------------------------+
//| Manage existing positions                                        |
//+------------------------------------------------------------------+
void ManagePositions(int index, string symbol)
{
    // Update position status for this symbol
    symbolData[index].inPosition = false;
    for(int i = 0; i < PositionsTotal(); i++)
    {
        if(PositionGetSymbol(i) == symbol)
        {
            symbolData[index].inPosition = true;
            break;
        }
    }
}

//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
{
    Print("🛑 Multi-Currency Profitable EA Stopped");
}