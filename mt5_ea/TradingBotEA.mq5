//+------------------------------------------------------------------+
//| TradingBotEA.mq5                                                 |
//| Expert Advisor for MT5 Signal Generation                        |
//| Sends signals to Python bot via webhook                         |
//+------------------------------------------------------------------+

#property copyright "Trading Bot System"
#property version   "1.00"
#property strict

// Input Parameters
input string    WebhookURL = "https://your-app.railway.app/webhook";  // Python bot webhook URL
input int       FastEMA = 9;           // Fast EMA period
input int       SlowEMA = 21;          // Slow EMA period
input int       TrendEMA = 200;        // Trend EMA period
input int       RSIPeriod = 14;        // RSI period
input double    RiskPercent = 1.0;     // Risk per trade (%)
input double    StopLossPercent = 2.0; // Stop loss (%)
input double    TakeProfitPercent = 4.0; // Take profit (%)
input bool      SendWebhooks = true;   // Send signals to Python bot
input bool      ExecuteOnMT5 = true;   // Execute trades on MT5 demo

// Global Variables
double fastEMA[], slowEMA, trendEMA[], rsi[];
int fastEMAHandle, slowEMAHandle, trendEMAHandle, rsiHandle;
datetime lastSignalTime = 0;
bool inPosition = false;
double entryPrice = 0;
string currentSymbol;

//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit()
{
    Print("🚀 Trading Bot EA Started");
    
    // Get current symbol
    currentSymbol = Symbol();
    
    // Initialize indicators
    fastEMAHandle = iMA(currentSymbol, PERIOD_M15, FastEMA, 0, MODE_EMA, PRICE_CLOSE);
    slowEMAHandle = iMA(currentSymbol, PERIOD_M15, SlowEMA, 0, MODE_EMA, PRICE_CLOSE);
    trendEMAHandle = iMA(currentSymbol, PERIOD_M15, TrendEMA, 0, MODE_EMA, PRICE_CLOSE);
    rsiHandle = iRSI(currentSymbol, PERIOD_M15, RSIPeriod, PRICE_CLOSE);
    
    if(fastEMAHandle == INVALID_HANDLE || slowEMAHandle == INVALID_HANDLE || 
       trendEMAHandle == INVALID_HANDLE || rsiHandle == INVALID_HANDLE)
    {
        Print("❌ Failed to initialize indicators");
        return INIT_FAILED;
    }
    
    Print("✅ Indicators initialized successfully");
    Print("📡 Webhook URL: ", WebhookURL);
    Print("📊 Symbol: ", currentSymbol);
    
    return INIT_SUCCEEDED;
}

//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
{
    // Check for new bar
    static datetime lastBarTime = 0;
    datetime currentBarTime = iTime(currentSymbol, PERIOD_M15, 0);
    
    if(currentBarTime == lastBarTime)
        return; // No new bar
    
    lastBarTime = currentBarTime;
    
    // Get indicator values
    if(!GetIndicatorValues())
        return;
    
    // Check for signals
    CheckForSignals();
    
    // Manage existing positions
    ManagePositions();
}

//+------------------------------------------------------------------+
//| Get indicator values                                             |
//+------------------------------------------------------------------+
bool GetIndicatorValues()
{
    // Resize arrays
    ArraySetAsSeries(fastEMA, true);
    ArraySetAsSeries(slowEMA, true);
    ArraySetAsSeries(trendEMA, true);
    ArraySetAsSeries(rsi, true);
    
    // Copy indicator values
    if(CopyBuffer(fastEMAHandle, 0, 0, 3, fastEMA) < 3 ||
       CopyBuffer(slowEMAHandle, 0, 0, 3, slowEMA) < 3 ||
       CopyBuffer(trendEMAHandle, 0, 0, 3, trendEMA) < 3 ||
       CopyBuffer(rsiHandle, 0, 0, 3, rsi) < 3)
    {
        Print("❌ Failed to copy indicator values");
        return false;
    }
    
    return true;
}

//+------------------------------------------------------------------+
//| Check for trading signals                                        |
//+------------------------------------------------------------------+
void CheckForSignals()
{
    double currentPrice = SymbolInfoDouble(currentSymbol, SYMBOL_BID);
    
    // Prevent multiple signals in short time
    if(TimeCurrent() - lastSignalTime < 300) // 5 minutes cooldown
        return;
    
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
        action, currentSymbol, price
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
    
    double lotSize = CalculateLotSize(price);
    double sl = price * (1 - StopLossPercent/100);
    double tp = price * (1 + TakeProfitPercent/100);
    
    MqlTradeRequest request;
    MqlTradeResult result;
    
    ZeroMemory(request);
    request.action = TRADE_ACTION_DEAL;
    request.symbol = currentSymbol;
    request.volume = lotSize;
    request.type = ORDER_TYPE_BUY;
    request.price = SymbolInfoDouble(currentSymbol, SYMBOL_ASK);
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
        if(PositionGetSymbol(i) == currentSymbol)
        {
            MqlTradeRequest request;
            MqlTradeResult result;
            
            ZeroMemory(request);
            request.action = TRADE_ACTION_DEAL;
            request.symbol = currentSymbol;
            request.volume = PositionGetDouble(POSITION_VOLUME);
            request.type = ORDER_TYPE_SELL;
            request.price = SymbolInfoDouble(currentSymbol, SYMBOL_BID);
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
//| Calculate lot size based on risk                                 |
//+------------------------------------------------------------------+
double CalculateLotSize(double price)
{
    double balance = AccountInfoDouble(ACCOUNT_BALANCE);
    double riskAmount = balance * RiskPercent / 100;
    double stopLossPoints = price * StopLossPercent / 100;
    double tickValue = SymbolInfoDouble(currentSymbol, SYMBOL_TRADE_TICK_VALUE);
    
    double lotSize = riskAmount / (stopLossPoints / SymbolInfoDouble(currentSymbol, SYMBOL_POINT) * tickValue);
    
    // Normalize lot size
    double minLot = SymbolInfoDouble(currentSymbol, SYMBOL_VOLUME_MIN);
    double maxLot = SymbolInfoDouble(currentSymbol, SYMBOL_VOLUME_MAX);
    double lotStep = SymbolInfoDouble(currentSymbol, SYMBOL_VOLUME_STEP);
    
    lotSize = MathMax(minLot, MathMin(maxLot, NormalizeDouble(lotSize/lotStep, 0) * lotStep));
    
    return lotSize;
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
        if(PositionGetSymbol(i) == currentSymbol)
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