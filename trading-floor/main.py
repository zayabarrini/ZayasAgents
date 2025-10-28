# main.py
import asyncio
import logging
from trading_floor import TradingFloor
from datetime import datetime
import json

async def main():
    """Main execution function for the Trading Floor"""
    print("🚀 Starting Agentic AI Trading Floor...")
    
    # Initialize trading floor
    trading_floor = TradingFloor(initial_capital=100000)
    
    print("✅ Trading Floor initialized with:")
    print(f"   - {len(trading_floor.agents)} Trading Agents")
    print(f"   - {len(trading_floor.mcp_servers)} MCP Servers")
    print(f"   - Initial Capital: ${trading_floor.initial_capital:,.2f}")
    
    # Run trading cycles
    num_cycles = 10  # Run 10 trading cycles for demonstration
    
    for cycle in range(num_cycles):
        print(f"\n📊 Running Trading Cycle {cycle + 1}/{num_cycles}")
        print("=" * 50)
        
        try:
            # Execute trading cycle
            results = await trading_floor.run_trading_cycle()
            
            # Display results
            await display_cycle_results(trading_floor, results, cycle + 1)
            
            # Wait between cycles (simulate real-time trading)
            await asyncio.sleep(5)
            
        except Exception as e:
            logging.error(f"Error in trading cycle {cycle + 1}: {e}")
            continue
    
    # Final performance report
    await generate_final_report(trading_floor)

async def display_cycle_results(trading_floor: TradingFloor, results: Any, cycle: int):
    """Display results from a trading cycle"""
    print(f"\n🔄 Cycle {cycle} Results:")
    print(f"   Available Capital: ${trading_floor.available_capital:,.2f}")
    print(f"   Active Positions: {len(trading_floor.positions)}")
    
    if trading_floor.performance_metrics:
        metrics = trading_floor.performance_metrics
        print(f"   Total Portfolio Value: ${metrics['total_portfolio_value']:,.2f}")
        print(f"   Total P&L: ${metrics['total_pnl']:,.2f}")
        print(f"   Return: {metrics['return_percentage']:.2f}%")
    
    # Show recent trades
    if hasattr(trading_floor, 'trade_history') and trading_floor.trade_history:
        recent_trades = trading_floor.trade_history[-3:]  # Last 3 trades
        print(f"   Recent Trades: {len(recent_trades)}")
        for trade in recent_trades:
            print(f"     - {trade['symbol']} {trade['action']} {trade['quantity']} shares")

async def generate_final_report(trading_floor: TradingFloor):
    """Generate final performance report"""
    print("\n" + "=" * 60)
    print("🎯 TRADING FLOOR FINAL PERFORMANCE REPORT")
    print("=" * 60)
    
    if trading_floor.performance_metrics:
        metrics = trading_floor.performance_metrics
        
        print(f"\n📈 Performance Summary:")
        print(f"   Initial Capital: ${trading_floor.initial_capital:,.2f}")
        print(f"   Final Portfolio Value: ${metrics['total_portfolio_value']:,.2f}")
        print(f"   Total Profit/Loss: ${metrics['total_pnl']:,.2f}")
        print(f"   Total Return: {metrics['return_percentage']:.2f}%")
        
        # Calculate annualized return (simplified)
        days_traded = 10  # Assuming 10 days of trading
        annualized_return = ((1 + metrics['return_percentage']/100) ** (252/days_traded) - 1) * 100
        print(f"   Annualized Return: {annualized_return:.2f}%")
    
    print(f"\n🔧 System Statistics:")
    print(f"   Total Trading Cycles: 10")
    print(f"   Active Positions: {len(trading_floor.positions)}")
    print(f"   Total Trades Executed: {len(trading_floor.trade_history)}")
    
    # Agent performance
    print(f"\n🤖 Agent Performance:")
    for agent_name, agent in trading_floor.agents.items():
        if hasattr(agent, 'performance_stats'):
            stats = agent.performance_stats
            print(f"   {agent_name.title().replace('_', ' ')}:")
            print(f"     - Signals Generated: {stats.get('signals_generated', 0)}")
            print(f"     - Trades Executed: {stats.get