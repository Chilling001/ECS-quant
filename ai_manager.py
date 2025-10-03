"""
AI Manager Module
Integrates OpenAI GPT as an AI portfolio manager for trade analysis and suggestions.
"""
from openai import OpenAI
from datetime import datetime
import json


class AIPortfolioManager:
    """
    AI Portfolio Manager using OpenAI GPT.
    Provides analysis on risk, diversification, and trading suggestions.
    """
    
    def __init__(self, api_key):
        """
        Initialize AI Portfolio Manager.
        
        Args:
            api_key: OpenAI API key
        """
        self.api_key = api_key
        self.client = OpenAI(api_key=api_key)
        self.conversation_history = []
        
    def analyze_portfolio(self, account_info, positions, recent_trades):
        """
        Analyze portfolio using AI.
        
        Args:
            account_info: Account balance and info
            positions: Current open positions
            recent_trades: Recent trade history
            
        Returns:
            AI analysis and suggestions
        """
        prompt = self._build_analysis_prompt(account_info, positions, recent_trades)
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert forex portfolio manager and risk analyst. Provide concise, actionable insights."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            analysis = response.choices[0].message.content
            self.conversation_history.append({
                'timestamp': datetime.now().isoformat(),
                'prompt': prompt,
                'response': analysis
            })
            
            return analysis
        except Exception as e:
            return f"Error getting AI analysis: {str(e)}"
    
    def _build_analysis_prompt(self, account_info, positions, recent_trades):
        """Build the prompt for AI analysis."""
        prompt = f"""
Analyze this forex trading portfolio:

ACCOUNT BALANCE:
- Total: ${account_info.get('balance', {}).get('total', 0):.2f}
- Free: ${account_info.get('balance', {}).get('free', 0):.2f}
- Used: ${account_info.get('balance', {}).get('used', 0):.2f}

OPEN POSITIONS:
{self._format_positions(positions)}

RECENT TRADES:
{self._format_trades(recent_trades)}

Provide analysis on:
1. Risk exposure and diversification
2. Position sizing appropriateness
3. Suggested actions or adjustments
4. Warning signs if any

Keep response under 200 words.
"""
        return prompt
    
    def _format_positions(self, positions):
        """Format positions for prompt."""
        if not positions:
            return "No open positions"
        
        formatted = []
        for symbol, pos in positions.items():
            formatted.append(f"- {symbol}: {pos.get('side', 'N/A')} {pos.get('contracts', 0)} units @ {pos.get('entryPrice', 0):.5f}")
        
        return "\n".join(formatted)
    
    def _format_trades(self, trades):
        """Format recent trades for prompt."""
        if not trades or len(trades) == 0:
            return "No recent trades"
        
        formatted = []
        for trade in trades[-5:]:  # Last 5 trades
            formatted.append(f"- {trade.get('symbol', 'N/A')}: {trade.get('side', 'N/A')} P&L: ${trade.get('pnl', 0):.2f}")
        
        return "\n".join(formatted)
    
    def chat_query(self, user_message, context=None):
        """
        General chat query to AI assistant.
        
        Args:
            user_message: User's question or message
            context: Optional context (account info, positions, etc.)
            
        Returns:
            AI response
        """
        messages = [
            {"role": "system", "content": "You are a knowledgeable forex trading assistant. Provide helpful, accurate information about forex trading, strategies, and risk management."}
        ]
        
        # Add context if provided
        if context:
            context_msg = f"Current context:\n{json.dumps(context, indent=2)}"
            messages.append({"role": "system", "content": context_msg})
        
        # Add recent conversation history (last 5 exchanges)
        for conv in self.conversation_history[-5:]:
            if 'user_message' in conv:
                messages.append({"role": "user", "content": conv['user_message']})
                messages.append({"role": "assistant", "content": conv['response']})
        
        # Add current message
        messages.append({"role": "user", "content": user_message})
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=300,
                temperature=0.7
            )
            
            ai_response = response.choices[0].message.content
            
            # Save to history
            self.conversation_history.append({
                'timestamp': datetime.now().isoformat(),
                'user_message': user_message,
                'response': ai_response
            })
            
            return ai_response
        except Exception as e:
            return f"Error: {str(e)}"
    
    def evaluate_trade_idea(self, symbol, side, entry_price, account_balance, current_positions):
        """
        Evaluate a trade idea before execution.
        
        Args:
            symbol: Trading pair
            side: 'buy' or 'sell'
            entry_price: Proposed entry price
            account_balance: Current account balance
            current_positions: Current open positions
            
        Returns:
            AI evaluation and recommendation
        """
        prompt = f"""
Evaluate this trade idea:
- Symbol: {symbol}
- Side: {side}
- Entry Price: {entry_price:.5f}
- Account Balance: ${account_balance:.2f}
- Current Positions: {len(current_positions)}

Consider:
1. Is this trade appropriate given current exposure?
2. Risk/reward assessment
3. Any concerns or red flags?

Provide brief recommendation (approve/caution/reject) with reasoning.
"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a forex risk manager. Evaluate trades critically."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.5
            )
            
            evaluation = response.choices[0].message.content
            return evaluation
        except Exception as e:
            return f"Error evaluating trade: {str(e)}"
    
    def get_conversation_history(self, limit=10):
        """Get recent conversation history."""
        return self.conversation_history[-limit:]
