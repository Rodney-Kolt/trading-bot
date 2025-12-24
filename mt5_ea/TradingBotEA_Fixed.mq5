//+------------------------------------------------------------------+
//| TradingBotEA_Fixed.mq5                                           |
//| Expert Advisor for MT5 Signal Generation - FIXED VERSION        |
//| Sends signals to Python bot via webhook                         |
//+------------------------------------------------------------------+

#property copyright "Trading Bot System"
#property version   "1.00"

// Input Parameters
input string    WebhookURL = "https://trading-bot-production-c863.up.railway.app/webhook";
input int       FastEMA = 9;
input int       SlowEMA = 21;
input int       TrendEMA = 200;
input int       RSIPeriod = 14;
input double    RiskPercent = 1.0;
input double    StopLossPercent = 2.0;
input double    TakeProfitPercent = 4.0;
input bool      SendWebhooks = true;
input bool      ExecuteOnMT5 = true;

// Global Variables
int fastEMAHandle, slowEMAHandle, trendEMAHandle, rsiHandle;
datetime lastSignalTime = 0;
bool inPosition = false;
double entryPrice = 0;

//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit()
{
    Print("🚀 Trading Bot EA Started");
    
    // Initialize indicators
    fastEMAHandle = iMA(_Symbol, PERIOD_M15, FastEMA, 0, MODE_EMA, PRICE_CLOSE);
    slowEMAHandle = iMA(_Symbol, PERIOD_M15, SlowEMA, 0, MODE_EMA, PRICE_CLOSE);
    trendEMAHandle = iMA(_Symbol, PERIOD_M15, TrendEMA, 0, MODE_EMA, PRICE_CLOSE);
    rsiHandle = iRSI(_Symbol, PERIOD_M15, RSIPeriod, PRICE_CLOSE);
    
    if(fastEMAHandle == INVALID_HANDLE || slowEMAHandle == INVALID_HANDLE || 
       trendEMAHandle == INVALID_HANDLE || rsiHandle == INVALID_HANDLE)
    {
        Print("❌ Failed to initialize indicators");
        return INIT_FAILED;
    }
    
    Print("✅ Indicators initialized successfully");
    Print("📡 Webhook URL: ", WebhookURL);
    Print("📊 Symbol: ", _Symbol);
    
    return INIT_SUCCEEDED;
}

//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
{
    // Check for new bar
    static datetime lastBarTime = 0;
    datetime currentBarTime = iTime(_Symbol, PERIOD_M15, 0);
    
    if(currentBarTime == lastBarTime)
        return;
    
    lastBarTime = currentBarTime;
    
    // Check for signals
    CheckForSignals();
    
    // Manage existing positions
    ManagePositions();
}

//+------------------------------------------------------------------+
//| Check for trading signals                                        |
//+------------------------------------------------------------------+
void CheckForSignals()
{
    double currentPrice = SymbolInfoDouble(_Symbol, SYMBOL_BID);
    
    // Prevent multiple signals in short time
    if(TimeCurrent() - lastSignalTime < 300) // 5 minutes cooldown
        return;
    
    // Get indicator values
    double fastEMA[], slowEMA[], trendEMA[], rsi[];
    
    ArraySetAsSeries(fastEMA, true);
    ArraySetAsSeries(slowEMA, true);
    ArraySetAsSeries(trendEMA, true);
    ArraySetAsSeries(rsi, true);
    
    if(CopyBuffer(fastEMAHandle, 0, 0, 3, fastEMA) < 3 ||
       CopyBuffer(slowEMAHandle, 0, 0, 3, slowEMA) < 3 ||
       CopyBuffer(trendEMAHandle, 0, 0, 3, trendEMA) < 3 ||
       CopyBuffer(rsiHandle, 0, 0, 3, rsi) < 3)
    {
        Print("❌ Failed to copy indicator values");
        return;
    }
    
    // BUY Signal Conditions
    bool buySignal = false;
    if(!inPosition && 
       currentPrice > trendEMA[0] &&           // Above trend EMA
       fastEMA[1] <= slowEMA[1] &&             // Previous: Fast EMA below Slow EMA
       fastEMA[0] > slowEMA[0] &&              // Current: Fast EMA above Slow EMA (crossover)
       rsi[0] < 70)                            // RSI not overbought
    {
        buySignal = true;
    }
    
    // SELL Signal Conditions  
    bool sellSignal = false;
    if(inPosition &&
       (currentPrice <= entryPrice * (1 - StopLossPercent/100) ||     // Stop loss hit
        currentPrice >= entryPrice * (1 + TakeProfitPercent/100) ||   // Take profit hit
        (fastEMA[1] >= slowEMA[1] && fastEMA[0] < slowEMA[0])))       // EMA crossunder
    {
        sellSignal = true;
    }
    
    // Execute signals
    if(buySignal)
    {
        ExecuteBuySignal(currentPrice);
    }
    else if(sellSignal)
    {
        ExecuteSellSignal(currentPrice);
    }
}

//+------------------------------------------------------------------+
//| Execute BUY signal                                               |
//+------------------------------------------------------------------+
void ExecuteBuySignal(double price)
{
    Print("🟢 BUY Signal Generated at ", price);
    
    // Send webhook to Python bot
    if(SendWebhooks)
    {
        SendWebhookSignal("BUY", price);
    }
    
    // Execute on MT5 demo
    if(ExecuteOnMT5)
    {
        ExecuteMT5Buy(price);
    }
    
    lastSignalTime = TimeCurrent();
}

//+------------------------------------------------------------------+
//| Execute SELL signal                                              |
//+------------------------------------------------------------------+
void ExecuteSellSignal(double price)
{
    Print("🔴 SELL Signal Generated at ", price);
    
    // Send webhook to Python bot
    if(SendWebhooks)
    {
        SendWebhookSignal("SELL", price);
    }
    
    // Execute on MT5 demo
    if(ExecuteOnMT5)
    {
        ExecuteMT5Sell(price);
    }
    
    lastSignalTime = TimeCurrent();
}

//+------------------------------------------------------------------+
//| Send webhook signal to Python bot                               |
//+------------------------------------------------------------------+
void SendWebhookSignal(string action, double price)
{
    string headers = "Content-Type: application/json\r\n";
    string data = StringFormat(
        "{\"action\":\"%s\",\"symbol\":\"%s\",\"price\":\"%.5f\",\"strategy\":\"MT5_EMA_RSI\",\"timeframe\":\"15m\"}",
        action, _Symbol, price
    );
    
    char post[], result[];
    StringToCharArray(data, post, 0, StringLen(data));
    
    int res = WebRequest("POST", WebhookURL, headers, 5000, post, result, headers);
    
    if(res == 200)
    {
        Print("✅ Webhook sent successfully: ", action, " at ", price);
    }
    else
    {
        Print("❌ Webhook failed. Code: ", res);
    }
}

//+------------------------------------------------------------------+
//| Execute BUY on MT5 demo                                          |
//+------------------------------------------------------------------+
void ExecuteMT5Buy(double price)
{
    if(inPosition)
        return;
    
    double lotSize = 0.01; // Fixed lot size for simplicity
    double sl = price * (1 - StopLossPercent/100);
    double tp = price * (1 + TakeProfitPercent/100);
    
    MqlTradeRequest request;
    MqlTradeResult result;
    
    ZeroMemory(request);
    request.action = TRADE_ACTION_DEAL;
    request.symbol = _Symbol;
    request.volume = lotSize;
    request.type = ORDER_TYPE_BUY;
    request.price = SymbolInfoDouble(_Symbol, SYMBOL_ASK);
    request.sl = sl;
    request.tp = tp;
    request.deviation = 10;
    request.magic = 123456;
    request.comment = "MT5 Bot Buy";
    
    if(OrderSend(request, result))
    {
        Print("✅ MT5 BUY executed: ", result.price, " SL:", sl, " TP:", tp);
        inPosition = true;
        entryPrice = result.price;
    }
    else
    {
        Print("❌ MT5 BUY failed: ", result.retcode);
    }
}

//+------------------------------------------------------------------+
//| Execute SELL on MT5 demo                                         |
//+------------------------------------------------------------------+
void ExecuteMT5Sell(double price)
{
    if(!inPosition)
        return;
    
    // Close position
    for(int i = PositionsTotal()-1; i >= 0; i--)
    {
        if(PositionGetSymbol(i) == _Symbol)
        {
            MqlTradeRequest request;
            MqlTradeResult result;
            
            ZeroMemory(request);
            request.action = TRADE_ACTION_DEAL;
            request.symbol = _Symbol;
            request.volume = PositionGetDouble(POSITION_VOLUME);
            request.type = ORDER_TYPE_SELL;
            request.price = SymbolInfoDouble(_Symbol, SYMBOL_BID);
            request.position = PositionGetInteger(POSITION_TICKET);
            request.magic = 123456;
            request.comment = "MT5 Bot Sell";
            
            if(OrderSend(request, result))
            {
                double pnl = result.price - entryPrice;
                Print("✅ MT5 SELL executed: ", result.price, " P&L: ", pnl);
                inPosition = false;
                entryPrice = 0;
            }
            break;
        }
    }
}

//+------------------------------------------------------------------+
//| Manage existing positions                                        |
//+------------------------------------------------------------------+
void ManagePositions()
{
    // Update position status
    inPosition = false;
    for(int i = 0; i < PositionsTotal(); i++)
    {
        if(PositionGetSymbol(i) == _Symbol)
        {
            inPosition = true;
            break;
        }
    }
}

//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
{
    Print("🛑 Trading Bot EA Stopped");
}