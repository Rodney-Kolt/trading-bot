//+------------------------------------------------------------------+
//| ProfitableEA_Clean.mq5                                          |
//| Small-Wins Automated Trading System - CLEAN VERSION            |
//| Focus: 0.5-1% per trade, strict risk management                 |
//+------------------------------------------------------------------+

#property copyright "Profitable Trading System"
#property version   "2.02"
#property description "Small-wins automated trading with strict risk controls"

//--- Input Parameters
input group "AUTOMATION CONTROL"
input bool      AutoTradingEnabled = false;    // Enable Auto Trading (START WITH FALSE!)
input bool      SendWebhooks = true;           // Send signals to Python bot
input string    WebhookURL = "https://trading-bot-production-c863.up.railway.app/webhook";

input group "RISK MANAGEMENT"
input double    RiskPercent = 0.5;             // Risk per trade (0.5% recommended)
input double    MaxDailyLoss = 2.0;            // Max daily loss % (HARD STOP)
input int       MaxTradesPerDay = 5;           // Max trades per day
input int       MaxConsecutiveLosses = 2;      // Stop after X losses

input group "STRATEGY SETTINGS"
input int       FastEMA = 9;                   // Fast EMA period
input int       SlowEMA = 21;                  // Slow EMA period
input int       TrendEMA = 200;                // Trend EMA period
input int       RSIPeriod = 14;                // RSI period
input double    StopLossPercent = 0.5;         // Stop Loss % (tight for scalping)
input double    TakeProfitPercent = 0.6;       // Take Profit % (1:1.2 RR)

input group "TRADING SESSIONS"
input bool      TradeLondonSession = true;     // Trade London (8-12 GMT)
input bool      TradeNYSession = true;         // Trade NY (13-17 GMT)
input bool      AvoidNews = true;              // Avoid major news times

//--- Global Variables
int fastEMAHandle = INVALID_HANDLE;
int slowEMAHandle = INVALID_HANDLE;
int trendEMAHandle = INVALID_HANDLE;
int rsiHandle = INVALID_HANDLE;

datetime lastTradeTime = 0;
datetime lastBarTime = 0;
int dailyTrades = 0;
double dailyPnL = 0.0;
int consecutiveLosses = 0;
datetime currentDate = 0;
bool emergencyStop = false;

//--- Trade tracking structure
struct TradeInfo {
    datetime openTime;
    double openPrice;
    double lotSize;
    string reason;
};
TradeInfo lastTrade;

//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit()
{
    Print("PROFITABLE EA STARTED - Small Wins System");
    Print("Auto Trading: ", AutoTradingEnabled ? "ENABLED" : "DISABLED");
    Print("Risk per trade: ", DoubleToString(RiskPercent, 1), "%");
    Print("Max daily loss: ", DoubleToString(MaxDailyLoss, 1), "%");
    
    // Initialize indicators
    fastEMAHandle = iMA(_Symbol, PERIOD_M15, FastEMA, 0, MODE_EMA, PRICE_CLOSE);
    slowEMAHandle = iMA(_Symbol, PERIOD_M15, SlowEMA, 0, MODE_EMA, PRICE_CLOSE);
    trendEMAHandle = iMA(_Symbol, PERIOD_M15, TrendEMA, 0, MODE_EMA, PRICE_CLOSE);
    rsiHandle = iRSI(_Symbol, PERIOD_M15, RSIPeriod, PRICE_CLOSE);
    
    if(fastEMAHandle == INVALID_HANDLE || slowEMAHandle == INVALID_HANDLE || 
       trendEMAHandle == INVALID_HANDLE || rsiHandle == INVALID_HANDLE)
    {
        Print("ERROR: Failed to initialize indicators");
        return(INIT_FAILED);
    }
    
    // Initialize daily tracking
    currentDate = TimeCurrent();
    ResetDailyCounters();
    
    Print("SUCCESS: Indicators initialized");
    Print("Symbol: ", _Symbol, " | Timeframe: M15");
    Print("Trading Sessions: London(", TradeLondonSession, ") NY(", TradeNYSession, ")");
    
    return(INIT_SUCCEEDED);
}

//+------------------------------------------------------------------+
//| Expert deinitialization function                                |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
{
    Print("Profitable EA Stopped - Reason: ", reason);
    Print("Final Stats: Trades=", dailyTrades, " | P&L=", DoubleToString(dailyPnL, 2), "% | Losses=", consecutiveLosses);
    
    // Release indicator handles
    if(fastEMAHandle != INVALID_HANDLE) IndicatorRelease(fastEMAHandle);
    if(slowEMAHandle != INVALID_HANDLE) IndicatorRelease(slowEMAHandle);
    if(trendEMAHandle != INVALID_HANDLE) IndicatorRelease(trendEMAHandle);
    if(rsiHandle != INVALID_HANDLE) IndicatorRelease(rsiHandle);
}

//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
{
    // Check for new day
    CheckNewDay();
    
    // Check for new bar
    datetime currentBarTime = iTime(_Symbol, PERIOD_M15, 0);
    if(currentBarTime == lastBarTime)
        return;
    lastBarTime = currentBarTime;
    
    // Check emergency stop conditions
    if(CheckEmergencyStop())
        return;
    
    // Check trading session
    if(!IsValidTradingSession())
        return;
    
    // Check for signals
    CheckForSignals();
    
    // Monitor open positions
    MonitorPositions();
}

//+------------------------------------------------------------------+
//| Check for new day and reset counters                            |
//+------------------------------------------------------------------+
void CheckNewDay()
{
    datetime today = TimeCurrent();
    MqlDateTime todayStruct, currentStruct;
    
    TimeToStruct(today, todayStruct);
    TimeToStruct(currentDate, currentStruct);
    
    if(todayStruct.day != currentStruct.day || todayStruct.month != currentStruct.month)
    {
        Print("New trading day - Resetting counters");
        Print("Yesterday: Trades=", dailyTrades, " P&L=", DoubleToString(dailyPnL, 2), "%");
        
        ResetDailyCounters();
        currentDate = today;
        emergencyStop = false;
    }
}

//+------------------------------------------------------------------+
//| Reset daily counters                                             |
//+------------------------------------------------------------------+
void ResetDailyCounters()
{
    dailyTrades = 0;
    dailyPnL = 0.0;
    consecutiveLosses = 0;
}

//+------------------------------------------------------------------+
//| Check emergency stop conditions                                 |
//+------------------------------------------------------------------+
bool CheckEmergencyStop()
{
    // Check daily loss limit
    if(dailyPnL <= -MaxDailyLoss)
    {
        if(!emergencyStop)
        {
            Print("EMERGENCY STOP: Daily loss limit reached (", DoubleToString(dailyPnL, 2), "%)");
            emergencyStop = true;
            SendEmergencyAlert("DAILY_LOSS_LIMIT");
        }
        return(true);
    }
    
    // Check consecutive losses
    if(consecutiveLosses >= MaxConsecutiveLosses)
    {
        if(!emergencyStop)
        {
            Print("EMERGENCY STOP: Too many consecutive losses (", consecutiveLosses, ")");
            emergencyStop = true;
            SendEmergencyAlert("CONSECUTIVE_LOSSES");
        }
        return(true);
    }
    
    // Check max trades per day
    if(dailyTrades >= MaxTradesPerDay)
    {
        if(!emergencyStop)
        {
            Print("DAILY LIMIT: Max trades reached (", dailyTrades, ")");
            emergencyStop = true;
        }
        return(true);
    }
    
    return(emergencyStop);
}

//+------------------------------------------------------------------+
//| Check if current time is valid for trading                      |
//+------------------------------------------------------------------+
bool IsValidTradingSession()
{
    MqlDateTime dt;
    TimeToStruct(TimeCurrent(), dt);
    
    int currentHour = dt.hour;
    
    // London Session: 8-12 GMT
    bool londonActive = TradeLondonSession && (currentHour >= 8 && currentHour < 12);
    
    // NY Session: 13-17 GMT  
    bool nyActive = TradeNYSession && (currentHour >= 13 && currentHour < 17);
    
    return(londonActive || nyActive);
}

//+------------------------------------------------------------------+
//| Check for trading signals                                        |
//+------------------------------------------------------------------+
void CheckForSignals()
{
    // Cooldown between trades (minimum 30 minutes)
    if(TimeCurrent() - lastTradeTime < 1800)
        return;
    
    // Don't trade if already in position
    if(PositionsTotal() > 0)
        return;
    
    // Get indicator values
    double fastEMA[3];
    double slowEMA[3];
    double trendEMA[3];
    double rsi[3];
    
    // Copy indicator buffers
    if(CopyBuffer(fastEMAHandle, 0, 0, 3, fastEMA) != 3 ||
       CopyBuffer(slowEMAHandle, 0, 0, 3, slowEMA) != 3 ||
       CopyBuffer(trendEMAHandle, 0, 0, 3, trendEMA) != 3 ||
       CopyBuffer(rsiHandle, 0, 0, 3, rsi) != 3)
    {
        Print("ERROR: Failed to copy indicator buffers");
        return;
    }
    
    // Set arrays as series (index 0 = current bar)
    ArraySetAsSeries(fastEMA, true);
    ArraySetAsSeries(slowEMA, true);
    ArraySetAsSeries(trendEMA, true);
    ArraySetAsSeries(rsi, true);
    
    double currentPrice = SymbolInfoDouble(_Symbol, SYMBOL_BID);
    if(currentPrice <= 0)
        return;
    
    // BUY Signal: EMA pullback in uptrend
    bool buySignal = false;
    string buyReason = "";
    
    if(currentPrice > trendEMA[0] &&                    // Above trend EMA (uptrend)
       fastEMA[1] <= slowEMA[1] &&                      // Previous: Fast below Slow
       fastEMA[0] > slowEMA[0] &&                       // Current: Fast above Slow (crossover)
       rsi[0] > 30 && rsi[0] < 70)                      // RSI in normal range
    {
        buySignal = true;
        buyReason = "EMA_CROSSOVER_UPTREND";
    }
    
    // SELL Signal: EMA pullback in downtrend
    bool sellSignal = false;
    string sellReason = "";
    
    if(currentPrice < trendEMA[0] &&                    // Below trend EMA (downtrend)
       fastEMA[1] >= slowEMA[1] &&                      // Previous: Fast above Slow
       fastEMA[0] < slowEMA[0] &&                       // Current: Fast below Slow (crossunder)
       rsi[0] > 30 && rsi[0] < 70)                      // RSI in normal range
    {
        sellSignal = true;
        sellReason = "EMA_CROSSUNDER_DOWNTREND";
    }
    
    // Execute signals
    if(buySignal)
    {
        ProcessSignal("BUY", currentPrice, buyReason);
    }
    else if(sellSignal)
    {
        ProcessSignal("SELL", currentPrice, sellReason);
    }
}

//+------------------------------------------------------------------+
//| Process trading signal                                           |
//+------------------------------------------------------------------+
void ProcessSignal(string action, double price, string reason)
{
    Print(action, " Signal: ", DoubleToString(price, _Digits), " | Reason: ", reason);
    
    // Always send webhook (for logging)
    if(SendWebhooks)
    {
        SendWebhookSignal(action, price, reason);
    }
    
    // Execute trade only if auto trading is enabled
    if(AutoTradingEnabled)
    {
        if(action == "BUY")
            ExecuteBuyTrade(price, reason);
        else if(action == "SELL")
            ExecuteSellTrade(price, reason);
    }
    else
    {
        Print("Auto trading disabled - Signal only mode");
    }
}

//+------------------------------------------------------------------+
//| Execute BUY trade                                                |
//+------------------------------------------------------------------+
void ExecuteBuyTrade(double price, string reason)
{
    double lotSize = CalculateLotSize();
    if(lotSize <= 0)
    {
        Print("ERROR: Invalid lot size calculated");
        return;
    }
    
    double ask = SymbolInfoDouble(_Symbol, SYMBOL_ASK);
    if(ask <= 0)
    {
        Print("ERROR: Invalid ASK price");
        return;
    }
    
    double sl = NormalizeDouble(ask * (1 - StopLossPercent/100), _Digits);
    double tp = NormalizeDouble(ask * (1 + TakeProfitPercent/100), _Digits);
    
    MqlTradeRequest request;
    MqlTradeResult result;
    
    ZeroMemory(request);
    request.action = TRADE_ACTION_DEAL;
    request.symbol = _Symbol;
    request.volume = lotSize;
    request.type = ORDER_TYPE_BUY;
    request.price = ask;
    request.sl = sl;
    request.tp = tp;
    request.deviation = 10;
    request.magic = 123456;
    request.comment = "ProfitableEA_" + reason;
    
    if(OrderSend(request, result))
    {
        Print("BUY executed: ", DoubleToString(result.price, _Digits), 
              " | SL:", DoubleToString(sl, _Digits), 
              " | TP:", DoubleToString(tp, _Digits), 
              " | Lot:", DoubleToString(lotSize, 2));
        
        // Update tracking
        dailyTrades++;
        lastTradeTime = TimeCurrent();
        
        // Store trade info
        lastTrade.openTime = TimeCurrent();
        lastTrade.openPrice = result.price;
        lastTrade.lotSize = lotSize;
        lastTrade.reason = reason;
        
        // Send trade confirmation
        SendTradeConfirmation("BUY", result.price, lotSize, sl, tp, reason);
    }
    else
    {
        Print("ERROR: BUY failed: ", result.retcode, " | ", result.comment);
    }
}

//+------------------------------------------------------------------+
//| Execute SELL trade                                               |
//+------------------------------------------------------------------+
void ExecuteSellTrade(double price, string reason)
{
    double lotSize = CalculateLotSize();
    if(lotSize <= 0)
    {
        Print("ERROR: Invalid lot size calculated");
        return;
    }
    
    double bid = SymbolInfoDouble(_Symbol, SYMBOL_BID);
    if(bid <= 0)
    {
        Print("ERROR: Invalid BID price");
        return;
    }
    
    double sl = NormalizeDouble(bid * (1 + StopLossPercent/100), _Digits);
    double tp = NormalizeDouble(bid * (1 - TakeProfitPercent/100), _Digits);
    
    MqlTradeRequest request;
    MqlTradeResult result;
    
    ZeroMemory(request);
    request.action = TRADE_ACTION_DEAL;
    request.symbol = _Symbol;
    request.volume = lotSize;
    request.type = ORDER_TYPE_SELL;
    request.price = bid;
    request.sl = sl;
    request.tp = tp;
    request.deviation = 10;
    request.magic = 123456;
    request.comment = "ProfitableEA_" + reason;
    
    if(OrderSend(request, result))
    {
        Print("SELL executed: ", DoubleToString(result.price, _Digits), 
              " | SL:", DoubleToString(sl, _Digits), 
              " | TP:", DoubleToString(tp, _Digits), 
              " | Lot:", DoubleToString(lotSize, 2));
        
        // Update tracking
        dailyTrades++;
        lastTradeTime = TimeCurrent();
        
        // Store trade info
        lastTrade.openTime = TimeCurrent();
        lastTrade.openPrice = result.price;
        lastTrade.lotSize = lotSize;
        lastTrade.reason = reason;
        
        // Send trade confirmation
        SendTradeConfirmation("SELL", result.price, lotSize, sl, tp, reason);
    }
    else
    {
        Print("ERROR: SELL failed: ", result.retcode, " | ", result.comment);
    }
}

//+------------------------------------------------------------------+
//| Calculate lot size based on risk percentage                     |
//+------------------------------------------------------------------+
double CalculateLotSize()
{
    double balance = AccountInfoDouble(ACCOUNT_BALANCE);
    if(balance <= 0)
        return(0);
    
    double riskAmount = balance * RiskPercent / 100;
    
    double tickValue = SymbolInfoDouble(_Symbol, SYMBOL_TRADE_TICK_VALUE);
    double tickSize = SymbolInfoDouble(_Symbol, SYMBOL_TRADE_TICK_SIZE);
    double currentPrice = SymbolInfoDouble(_Symbol, SYMBOL_BID);
    
    if(tickValue <= 0 || tickSize <= 0 || currentPrice <= 0)
        return(0);
    
    double stopLossPoints = currentPrice * StopLossPercent / 100;
    double stopLossTicks = stopLossPoints / tickSize;
    
    if(stopLossTicks <= 0)
        return(0);
    
    double lotSize = riskAmount / (stopLossTicks * tickValue);
    
    // Normalize lot size
    double minLot = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MIN);
    double maxLot = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MAX);
    double lotStep = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_STEP);
    
    if(lotStep > 0)
        lotSize = NormalizeDouble(MathRound(lotSize/lotStep) * lotStep, 2);
    
    lotSize = MathMax(minLot, MathMin(maxLot, lotSize));
    
    return(lotSize);
}

//+------------------------------------------------------------------+
//| Monitor open positions                                           |
//+------------------------------------------------------------------+
void MonitorPositions()
{
    int total = PositionsTotal();
    for(int i = 0; i < total; i++)
    {
        ulong ticket = PositionGetTicket(i);
        if(ticket > 0 && PositionSelectByTicket(ticket))
        {
            if(PositionGetString(POSITION_SYMBOL) == _Symbol)
            {
                // Position found - it will be closed by SL/TP automatically
                // We just need to track when it closes for P&L calculation
            }
        }
    }
}

//+------------------------------------------------------------------+
//| Send webhook signal to Python bot                               |
//+------------------------------------------------------------------+
void SendWebhookSignal(string action, double price, string reason)
{
    string headers = "Content-Type: application/json\r\n";
    string data = StringFormat(
        "{\"action\":\"%s\",\"symbol\":\"%s\",\"price\":\"%.5f\",\"strategy\":\"PROFITABLE_EA\",\"reason\":\"%s\",\"timeframe\":\"15m\",\"auto_trading\":%s}",
        action, _Symbol, price, reason, AutoTradingEnabled ? "true" : "false"
    );
    
    char post[];
    char result[];
    string headers_result;
    
    StringToCharArray(data, post, 0, StringLen(data));
    
    int res = WebRequest("POST", WebhookURL, headers, 5000, post, result, headers_result);
    
    if(res == 200)
    {
        Print("Webhook sent: ", action, " | ", reason);
    }
    else
    {
        Print("Webhook failed: ", res);
    }
}

//+------------------------------------------------------------------+
//| Send trade confirmation to Python bot                           |
//+------------------------------------------------------------------+
void SendTradeConfirmation(string action, double price, double lotSize, double sl, double tp, string reason)
{
    string headers = "Content-Type: application/json\r\n";
    string data = StringFormat(
        "{\"action\":\"TRADE_EXECUTED\",\"symbol\":\"%s\",\"side\":\"%s\",\"price\":\"%.5f\",\"lot_size\":\"%.2f\",\"stop_loss\":\"%.5f\",\"take_profit\":\"%.5f\",\"reason\":\"%s\",\"daily_trades\":%d}",
        _Symbol, action, price, lotSize, sl, tp, reason, dailyTrades
    );
    
    char post[];
    char result[];
    string headers_result;
    
    StringToCharArray(data, post, 0, StringLen(data));
    
    WebRequest("POST", WebhookURL, headers, 5000, post, result, headers_result);
}

//+------------------------------------------------------------------+
//| Send emergency alert                                             |
//+------------------------------------------------------------------+
void SendEmergencyAlert(string alertType)
{
    string headers = "Content-Type: application/json\r\n";
    string data = StringFormat(
        "{\"action\":\"EMERGENCY_STOP\",\"alert_type\":\"%s\",\"daily_pnl\":\"%.2f\",\"daily_trades\":%d,\"consecutive_losses\":%d}",
        alertType, dailyPnL, dailyTrades, consecutiveLosses
    );
    
    char post[];
    char result[];
    string headers_result;
    
    StringToCharArray(data, post, 0, StringLen(data));
    
    WebRequest("POST", WebhookURL, headers, 5000, post, result, headers_result);
}

//+------------------------------------------------------------------+
//| Trade transaction event                                          |
//+------------------------------------------------------------------+
void OnTradeTransaction(const MqlTradeTransaction& trans,
                       const MqlTradeRequest& request,
                       const MqlTradeResult& result)
{
    // Track when positions close to calculate P&L
    if(trans.type == TRADE_TRANSACTION_DEAL_ADD)
    {
        if(trans.symbol == _Symbol)
        {
            double profit = trans.profit;
            if(profit != 0) // Position closed
            {
                double balance = AccountInfoDouble(ACCOUNT_BALANCE);
                if(balance > 0)
                {
                    double profitPercent = (profit / balance) * 100;
                    dailyPnL += profitPercent;
                    
                    if(profit > 0)
                    {
                        consecutiveLosses = 0; // Reset on win
                        Print("Trade closed: +", DoubleToString(profitPercent, 3), "% | Daily P&L: ", DoubleToString(dailyPnL, 2), "%");
                    }
                    else
                    {
                        consecutiveLosses++;
                        Print("Trade closed: ", DoubleToString(profitPercent, 3), "% | Consecutive losses: ", consecutiveLosses);
                    }
                    
                    // Send P&L update
                    SendPnLUpdate(profitPercent, profit > 0);
                }
            }
        }
    }
}

//+------------------------------------------------------------------+
//| Send P&L update to Python bot                                   |
//+------------------------------------------------------------------+
void SendPnLUpdate(double profitPercent, bool isWin)
{
    string headers = "Content-Type: application/json\r\n";
    string data = StringFormat(
        "{\"action\":\"TRADE_CLOSED\",\"symbol\":\"%s\",\"profit_percent\":\"%.3f\",\"is_win\":%s,\"daily_pnl\":\"%.2f\",\"consecutive_losses\":%d}",
        _Symbol, profitPercent, isWin ? "true" : "false", dailyPnL, consecutiveLosses
    );
    
    char post[];
    char result[];
    string headers_result;
    
    StringToCharArray(data, post, 0, StringLen(data));
    
    WebRequest("POST", WebhookURL, headers, 5000, post, result, headers_result);
}