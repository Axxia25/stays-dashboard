import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta, date
import requests
from faker import Faker
import time

# Configuração da página
st.set_page_config(
    page_title="Stays Analytics | Premium Dashboard Suite",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado elegante
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Reset e base */
    .main {
        padding-top: 0rem;
    }
    
    /* Fonte personalizada */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Header elegante */
    .elegant-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 3rem;
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .elegant-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: pulse 4s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 0.5; }
        50% { transform: scale(1.05); opacity: 0.8; }
    }
    
    .elegant-header h1 {
        color: white;
        font-size: 3.5rem;
        font-weight: 700;
        margin: 0 0 1rem 0;
        text-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        position: relative;
        z-index: 1;
    }
    
    .elegant-header p {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.3rem;
        margin: 0;
        font-weight: 400;
        position: relative;
        z-index: 1;
    }
    
    /* Cards de métricas premium */
    .premium-metric-card {
        background: white;
        border-radius: 20px;
        padding: 2.5rem 2rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(230, 230, 235, 0.5);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
        margin-bottom: 1.5rem;
    }
    
    .premium-metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.12);
    }
    
    .premium-metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2);
    }
    
    .metric-icon {
        width: 60px;
        height: 60px;
        border-radius: 15px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        margin-bottom: 1.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        box-shadow: 0 8px 16px rgba(102, 126, 234, 0.3);
    }
    
    .metric-title {
        font-size: 0.95rem;
        font-weight: 600;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
    }
    
    .metric-value {
        font-size: 2.8rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 0.5rem;
        line-height: 1;
    }
    
    .metric-change {
        font-size: 0.9rem;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        backdrop-filter: blur(10px);
    }
    
    .metric-change.positive {
        background: rgba(34, 197, 94, 0.1);
        color: #16a34a;
    }
    
    .metric-change.negative {
        background: rgba(239, 68, 68, 0.1);
        color: #dc2626;
    }
    
    /* Seção elegante */
    .elegant-section {
        background: white;
        border-radius: 20px;
        padding: 2.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.06);
        border: 1px solid rgba(230, 230, 235, 0.5);
    }
    
    .section-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 2rem;
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .section-title::before {
        content: '';
        width: 6px;
        height: 40px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 3px;
    }
    
    /* Sidebar elegante */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
        border-right: 1px solid #e2e8f0;
    }
    
    /* Filtros premium */
    .filter-container {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        border: 1px solid rgba(230, 230, 235, 0.5);
    }
    
    .filter-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #475569;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Cards de propriedade elegantes */
    .property-card-premium {
        background: white;
        border-radius: 16px;
        padding: 1.8rem;
        margin-bottom: 1.2rem;
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .property-card-premium:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
    }
    
    .property-card-premium.high-performance::before {
        content: '';
        position: absolute;
        left: 0;
        top: 0;
        width: 6px;
        height: 100%;
        background: linear-gradient(180deg, #10b981 0%, #059669 100%);
    }
    
    .property-card-premium.medium-performance::before {
        content: '';
        position: absolute;
        left: 0;
        top: 0;
        width: 6px;
        height: 100%;
        background: linear-gradient(180deg, #f59e0b 0%, #d97706 100%);
    }
    
    .property-card-premium.low-performance::before {
        content: '';
        position: absolute;
        left: 0;
        top: 0;
        width: 6px;
        height: 100%;
        background: linear-gradient(180deg, #ef4444 0%, #dc2626 100%);
    }
    
    .property-name {
        font-size: 1.2rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 0.8rem;
    }
    
    .property-metrics {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 1rem;
    }
    
    .property-occupancy {
        font-size: 2rem;
        font-weight: 800;
        line-height: 1;
    }
    
    .property-details {
        text-align: right;
        color: #64748b;
        font-size: 0.9rem;
    }
    
    /* Alertas elegantes */
    .alert-premium {
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: none;
        position: relative;
        backdrop-filter: blur(10px);
    }
    
    .alert-premium.success {
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.1) 0%, rgba(21, 128, 61, 0.05) 100%);
        border-left: 4px solid #10b981;
        color: #166534;
    }
    
    .alert-premium.warning {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.1) 0%, rgba(217, 119, 6, 0.05) 100%);
        border-left: 4px solid #f59e0b;
        color: #92400e;
    }
    
    .alert-premium.danger {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(220, 38, 38, 0.05) 100%);
        border-left: 4px solid #ef4444;
        color: #991b1b;
    }
    
    .alert-title {
        font-weight: 700;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
    }
    
    /* Tabs elegantes */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: #f8fafc;
        border-radius: 12px;
        padding: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 3rem;
        border-radius: 8px;
        font-weight: 600;
        color: #64748b;
        background: transparent;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: white !important;
        color: #1e293b !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    
    /* Botão reserva urgente */
    .urgent-booking {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%);
        color: white;
        padding: 1rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        font-weight: 600;
        border: none;
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3);
    }
    
    /* Cards de status */
    .status-card {
        padding: 1rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        border-left: 4px solid;
    }
    
    .status-confirmed { border-left-color: #10b981; background: rgba(16, 185, 129, 0.05); }
    .status-pending { border-left-color: #f59e0b; background: rgba(245, 158, 11, 0.05); }
    .status-canceled { border-left-color: #ef4444; background: rgba(239, 68, 68, 0.05); }
</style>
""", unsafe_allow_html=True)

# Funções de dados (expandidas para suportar todos os dashboards)
@st.cache_data(ttl=300)
def generate_stays_comprehensive_data():
    """Gera dataset completo para todos os dashboards"""
    fake = Faker('pt_PT')
    np.random.seed(42)
    
    # Propriedades expandidas com mais dados
    properties = [
        {"id": "LU01F", "name": "Vibe República Premium", "type": "entire_place", "region": "São Paulo", "city": "São Paulo", "rooms": 45, "status": "active"},
        {"id": "CP02A", "name": "Copacabana Luxury Suite", "type": "entire_place", "region": "Rio de Janeiro", "city": "Rio de Janeiro", "rooms": 32, "status": "active"},
        {"id": "IP03B", "name": "Ipanema Ocean View", "type": "private_room", "region": "Rio de Janeiro", "city": "Rio de Janeiro", "rooms": 28, "status": "active"},
        {"id": "CE04C", "name": "Centro Business Hub", "type": "entire_place", "region": "São Paulo", "city": "São Paulo", "rooms": 38, "status": "active"},
        {"id": "VM05D", "name": "Vila Madalena Loft", "type": "entire_place", "region": "São Paulo", "city": "São Paulo", "rooms": 25, "status": "active"},
        {"id": "LE06E", "name": "Leblon Beachfront", "type": "private_room", "region": "Rio de Janeiro", "city": "Rio de Janeiro", "rooms": 22, "status": "active"},
        {"id": "PI07F", "name": "Pinheiros Modern", "type": "entire_place", "region": "São Paulo", "city": "São Paulo", "rooms": 35, "status": "maintenance"},
        {"id": "BO08G", "name": "Botafogo Panoramic", "type": "private_room", "region": "Rio de Janeiro", "city": "Rio de Janeiro", "rooms": 30, "status": "active"},
    ]
    
    # Dados de clientes recorrentes
    recurring_clients = []
    for i in range(50):
        client = {
            "client_id": f"CLI{i+1:03d}",
            "name": fake.name(),
            "email": fake.email(),
            "phone": fake.phone_number(),
            "country": np.random.choice(["Brasil", "Argentina", "EUA", "França", "Alemanha"], p=[0.4, 0.15, 0.15, 0.15, 0.15]),
            "vip_status": np.random.choice(["Gold", "Silver", "Bronze", "Regular"], p=[0.1, 0.2, 0.3, 0.4]),
            "total_bookings": np.random.randint(1, 15),
            "lifetime_value": np.random.randint(1000, 25000)
        }
        recurring_clients.append(client)
    
    # Gerar reservas dos últimos 8 meses
    bookings = []
    start_date = datetime.now() - timedelta(days=240)
    
    for i in range(650):
        property_data = np.random.choice(properties)
        client_data = np.random.choice(recurring_clients)
        
        check_in = start_date + timedelta(days=np.random.randint(0, 240))
        stay_duration = np.random.randint(1, 12)
        check_out = check_in + timedelta(days=stay_duration)
        
        # Preços baseados na região, tipo e sazonalidade
        base_prices = {
            ("Rio de Janeiro", "entire_place"): 450,
            ("Rio de Janeiro", "private_room"): 240,
            ("São Paulo", "entire_place"): 380,
            ("São Paulo", "private_room"): 200
        }
        
        base_price = base_prices.get((property_data["region"], property_data["type"]), 280)
        
        # Fatores de variação de preço
        seasonal_factor = 1.4 if check_in.month in [12, 1, 2, 6, 7] else 1.0
        weekend_factor = 1.5 if check_in.weekday() >= 5 else 1.0
        vip_factor = 1.2 if client_data["vip_status"] in ["Gold", "Silver"] else 1.0
        price_variation = np.random.uniform(0.8, 1.8)
        
        total_price = base_price * stay_duration * seasonal_factor * weekend_factor * vip_factor * price_variation
        
        # Status da reserva com pesos realistas
        booking_status = np.random.choice(
            ["confirmed", "pending", "canceled", "checked_in", "checked_out", "no_show"], 
            p=[0.75, 0.08, 0.04, 0.05, 0.07, 0.01]
        )
        
        booking = {
            "id": f"RES{i+1:04d}",
            "property_id": property_data["id"],
            "property_name": property_data["name"],
            "property_type": property_data["type"],
            "property_status": property_data["status"],
            "region": property_data["region"],
            "city": property_data["city"],
            "check_in": check_in,
            "check_out": check_out,
            "guests": np.random.randint(1, 6),
            "nights": stay_duration,
            "total_price": round(total_price, 2),
            "daily_rate": round(total_price / stay_duration, 2),
            "status": booking_status,
            "client_id": client_data["client_id"],
            "client_name": client_data["name"],
            "client_email": client_data["email"],
            "client_country": client_data["country"],
            "client_vip": client_data["vip_status"],
            "booking_date": check_in - timedelta(days=np.random.randint(1, 60)),
            "source": np.random.choice(["Direct", "Booking.com", "Airbnb", "Expedia", "Google", "Instagram"], p=[0.35, 0.25, 0.2, 0.1, 0.05, 0.05]),
            "payment_method": np.random.choice(["Credit Card", "PIX", "Bank Transfer", "PayPal"], p=[0.5, 0.3, 0.15, 0.05]),
            "special_requests": np.random.choice(["None", "Late Check-in", "Early Check-out", "Extra Bed", "Airport Transfer"], p=[0.6, 0.15, 0.15, 0.05, 0.05])
        }
        bookings.append(booking)
    
    return pd.DataFrame(bookings), properties, recurring_clients

@st.cache_data(ttl=300)
def generate_promotional_codes():
    """Gera dados expandidos de códigos promocionais"""
    codes = [
        {"code": "PREMIUM25", "discount": 25, "type": "percent", "uses": 234, "max_uses": 300, "revenue_impact": 156800, "discount_given": 39200, "active": True, "start_date": "2025-01-01", "end_date": "2025-12-31"},
        {"code": "EXECUTIVO15", "discount": 15, "type": "percent", "uses": 189, "max_uses": 250, "revenue_impact": 98400, "discount_given": 23100, "active": True, "start_date": "2025-01-01", "end_date": "2025-12-31"},
        {"code": "NEGOCIOS30", "discount": 30, "type": "percent", "uses": 145, "max_uses": 200, "revenue_impact": 87600, "discount_given": 37500, "active": True, "start_date": "2025-01-01", "end_date": "2025-06-30"},
        {"code": "FIDELIDADE", "discount": 150, "type": "fixed", "uses": 89, "max_uses": 150, "revenue_impact": 45300, "discount_given": 13350, "active": True, "start_date": "2025-01-01", "end_date": "2025-12-31"},
        {"code": "TEMPORADA40", "discount": 40, "type": "percent", "uses": 67, "max_uses": 100, "revenue_impact": 34200, "discount_given": 22800, "active": False, "start_date": "2024-12-01", "end_date": "2025-02-28"},
        {"code": "WEEKEND50", "discount": 50, "type": "fixed", "uses": 123, "max_uses": 200, "revenue_impact": 56700, "discount_given": 6150, "active": True, "start_date": "2025-01-01", "end_date": "2025-12-31"},
        {"code": "FAMILIA20", "discount": 20, "type": "percent", "uses": 178, "max_uses": 300, "revenue_impact": 78900, "discount_given": 19725, "active": True, "start_date": "2025-01-01", "end_date": "2025-12-31"}
    ]
    return pd.DataFrame(codes)

def calculate_comprehensive_kpis(df):
    """Calcula KPIs abrangentes para todos os dashboards"""
    current_month = datetime.now().replace(day=1)
    last_month = (current_month - timedelta(days=1)).replace(day=1)
    
    current_data = df[df['check_in'] >= current_month]
    last_month_data = df[(df['check_in'] >= last_month) & (df['check_in'] < current_month)]
    
    kpis = {}
    
    # KPIs financeiros
    kpis['revenue'] = current_data['total_price'].sum()
    kpis['revenue_last'] = last_month_data['total_price'].sum()
    kpis['revenue_change'] = ((kpis['revenue'] - kpis['revenue_last']) / kpis['revenue_last']) * 100 if kpis['revenue_last'] > 0 else 0
    
    kpis['adr'] = current_data['daily_rate'].mean() if not current_data.empty else 0
    kpis['adr_last'] = last_month_data['daily_rate'].mean() if not last_month_data.empty else 0
    kpis['adr_change'] = ((kpis['adr'] - kpis['adr_last']) / kpis['adr_last']) * 100 if kpis['adr_last'] > 0 else 0
    
    # KPIs operacionais
    kpis['bookings'] = len(current_data)
    kpis['bookings_last'] = len(last_month_data)
    kpis['bookings_change'] = ((kpis['bookings'] - kpis['bookings_last']) / kpis['bookings_last']) * 100 if kpis['bookings_last'] > 0 else 0
    
    # Taxa de ocupação
    total_rooms = 255  # Total de quartos das propriedades
    days_in_month = datetime.now().day
    kpis['occupancy'] = (current_data['nights'].sum() / (total_rooms * days_in_month)) * 100
    
    last_month_days = (current_month - timedelta(days=1)).day
    kpis['occupancy_last'] = (last_month_data['nights'].sum() / (total_rooms * last_month_days)) * 100
    kpis['occupancy_change'] = kpis['occupancy'] - kpis['occupancy_last']
    
    # RevPAR
    kpis['revpar'] = kpis['revenue'] / (total_rooms * days_in_month) if days_in_month > 0 else 0
    kpis['revpar_last'] = kpis['revenue_last'] / (total_rooms * last_month_days) if last_month_days > 0 else 0
    kpis['revpar_change'] = ((kpis['revpar'] - kpis['revpar_last']) / kpis['revpar_last']) * 100 if kpis['revpar_last'] > 0 else 0
    
    # KPIs de customer experience
    kpis['avg_stay'] = current_data['nights'].mean() if not current_data.empty else 0
    kpis['cancellation_rate'] = (len(current_data[current_data['status'] == 'canceled']) / len(current_data)) * 100 if len(current_data) > 0 else 0
    kpis['vip_bookings'] = len(current_data[current_data['client_vip'].isin(['Gold', 'Silver'])])
    
    return kpis

def create_elegant_metric_card(title, value, change, icon):
    """Cria card de métrica elegante"""
    change_class = "positive" if change >= 0 else "negative"
    change_symbol = "↗" if change >= 0 else "↘"
    
    return f"""
    <div class="premium-metric-card">
        <div class="metric-icon">{icon}</div>
        <div class="metric-title">{title}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-change {change_class}">
            {change_symbol} {abs(change):.1f}%
        </div>
    </div>
    """

def create_revenue_evolution_chart(df):
    """Gráfico de evolução da receita mensal"""
    df['month'] = df['check_in'].dt.to_period('M')
    monthly_data = df.groupby('month').agg({
        'total_price': 'sum',
        'id': 'count',
        'daily_rate': 'mean'
    }).reset_index()
    
    monthly_data['month_str'] = monthly_data['month'].astype(str)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=monthly_data['month_str'],
        y=monthly_data['total_price'],
        mode='lines+markers',
        name='Receita Mensal',
        line=dict(color='rgba(102, 126, 234, 1)', width=4, shape='spline'),
        marker=dict(size=12, color='rgba(102, 126, 234, 1)', line=dict(color='white', width=3)),
        fill='tonexty',
        fillcolor='rgba(102, 126, 234, 0.1)',
        hovertemplate='<b>%{x}</b><br>Receita: R$ %{y:,.0f}<extra></extra>'
    ))
    
    fig.update_layout(
        title={'text': '<b>Evolução da Receita Mensal</b>', 'font': {'size': 24, 'family': 'Inter'}, 'x': 0.02},
        xaxis_title="Período", yaxis_title="Receita (R$)", height=400,
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter", size=14), hovermode='x unified', showlegend=False
    )
    
    fig.update_xaxes(gridcolor='rgba(0,0,0,0.05)', showgrid=True, zeroline=False)
    fig.update_yaxes(gridcolor='rgba(0,0,0,0.05)', showgrid=True, zeroline=False, tickformat=',.0f')
    
    return fig

def create_occupancy_heatmap_fixed(df):
    """Cria mapa de calor de ocupação (versão corrigida)"""
    df['day_of_week'] = df['check_in'].dt.day_name()
    df['week'] = df['check_in'].dt.isocalendar().week
    
    occupancy_data = df.groupby(['week', 'day_of_week']).size().reset_index(name='bookings')
    
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    occupancy_pivot = occupancy_data.pivot(index='week', columns='day_of_week', values='bookings').fillna(0)
    occupancy_pivot = occupancy_pivot.reindex(columns=weekdays)
    
    fig = go.Figure(data=go.Heatmap(
        z=occupancy_pivot.values,
        x=['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom'],
        y=occupancy_pivot.index,
        colorscale=[[0, '#f8fafc'], [1, '#667eea']],
        showscale=True,
        colorbar=dict(title="Reservas"),
        hoverongaps=False,
        hovertemplate='Semana %{y}<br>%{x}: %{z} reservas<extra></extra>'
    ))
    
    fig.update_layout(
        title={'text': '<b>Padrão de Ocupação Semanal</b>', 'font': {'size': 20, 'family': 'Inter'}, 'x': 0.02},
        xaxis_title="Dia da Semana", yaxis_title="Semana do Ano", height=400,
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter", size=12)
    )
    
    return fig

def create_property_performance_chart(df):
    """Gráfico de performance por propriedade"""
    property_stats = df.groupby('property_name').agg({
        'total_price': 'sum',
        'daily_rate': 'mean',
        'id': 'count'
    }).reset_index()
    
    property_stats = property_stats.sort_values('total_price', ascending=True)
    
    fig = go.Figure(go.Bar(
        y=property_stats['property_name'],
        x=property_stats['total_price'],
        orientation='h',
        marker=dict(
            color=property_stats['total_price'],
            colorscale=[[0, '#667eea'], [1, '#764ba2']],
            line=dict(color='rgba(255,255,255,0.2)', width=1)
        ),
        text=[f'R$ {x:,.0f}' for x in property_stats['total_price']],
        textposition='auto',
        hovertemplate='<b>%{y}</b><br>Receita: R$ %{x:,.0f}<extra></extra>'
    ))
    
    fig.update_layout(
        title={'text': '<b>Receita por Propriedade</b>', 'font': {'size': 20, 'family': 'Inter'}, 'x': 0.02},
        xaxis_title="Receita Total (R$)", height=400,
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter", size=12)
    )
    
    fig.update_xaxes(gridcolor='rgba(0,0,0,0.05)', showgrid=True, zeroline=False, tickformat=',.0f')
    fig.update_yaxes(gridcolor='rgba(0,0,0,0.05)', showgrid=False)
    
    return fig

# Interface principal com todos os dashboards
def main():
    # Header elegante
    st.markdown("""
    <div class="elegant-header">
        <h1>Stays Analytics Suite</h1>
        <p>Plataforma Completa de Business Intelligence Hoteleira</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Carregamento de dados
    with st.spinner('🚀 Carregando dados integrados...'):
        df_bookings, properties, clients = generate_stays_comprehensive_data()
        df_promos = generate_promotional_codes()
        time.sleep(0.5)
    
    # Sidebar com filtros globais
    with st.sidebar:
        st.markdown('<div class="filter-container">', unsafe_allow_html=True)
        st.markdown('<div class="filter-title">🎯 Filtros Globais</div>', unsafe_allow_html=True)
        
        date_range = st.date_input(
            "📅 Período de Análise",
            value=[datetime.now() - timedelta(days=30), datetime.now()],
            max_value=datetime.now()
        )
        
        regions = st.multiselect(
            "🏙️ Regiões",
            options=df_bookings['region'].unique(),
            default=df_bookings['region'].unique()
        )
        
        property_types = st.multiselect(
            "🏨 Tipos de Propriedade",
            options=df_bookings['property_type'].unique(),
            default=df_bookings['property_type'].unique()
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Insight rápido
        st.markdown('<div class="filter-container">', unsafe_allow_html=True)
        st.markdown('<div class="filter-title">⚡ Dashboard Ativo</div>', unsafe_allow_html=True)
        
        dashboard_selection = st.selectbox(
            "Selecione o Dashboard:",
            [
                "📊 Visão Executiva",
                "🏨 Dashboard Operacional", 
                "💰 Analytics Financeiro",
                "📋 Central de Propriedades",
                "🎁 Códigos Promocionais",
                "👥 Análise de Clientes",
                "🔍 Business Intelligence"
            ]
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Filtrar dados globalmente
    filtered_df = df_bookings[
        (df_bookings['check_in'] >= pd.to_datetime(date_range[0])) &
        (df_bookings['check_in'] <= pd.to_datetime(date_range[1])) &
        (df_bookings['region'].isin(regions)) &
        (df_bookings['property_type'].isin(property_types))
    ]
    
    # Calcular KPIs
    kpis = calculate_comprehensive_kpis(df_bookings)
    
    # Renderizar dashboard selecionado
    if dashboard_selection == "📊 Visão Executiva":
        render_executive_dashboard(filtered_df, kpis, df_promos)
    elif dashboard_selection == "🏨 Dashboard Operacional":
        render_operational_dashboard(filtered_df, properties)
    elif dashboard_selection == "💰 Analytics Financeiro":
        render_financial_analytics(filtered_df, kpis)
    elif dashboard_selection == "📋 Central de Propriedades":
        render_property_central(filtered_df, properties)
    elif dashboard_selection == "🎁 Códigos Promocionais":
        render_promo_codes_dashboard(df_promos, filtered_df)
    elif dashboard_selection == "👥 Análise de Clientes":
        render_customer_analytics(filtered_df, clients)
    elif dashboard_selection == "🔍 Business Intelligence":
        render_business_intelligence(filtered_df, kpis)

def render_executive_dashboard(df, kpis, promos):
    """Dashboard Executivo - Visão Geral"""
    st.markdown("## 📊 Dashboard Executivo")
    
    # KPIs principais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(create_elegant_metric_card("Receita Total", f"R$ {kpis['revenue']:,.0f}", kpis['revenue_change'], "💰"), unsafe_allow_html=True)
    
    with col2:
        st.markdown(create_elegant_metric_card("ADR Médio", f"R$ {kpis['adr']:,.0f}", kpis['adr_change'], "📊"), unsafe_allow_html=True)
    
    with col3:
        st.markdown(create_elegant_metric_card("Ocupação", f"{kpis['occupancy']:.1f}%", kpis['occupancy_change'], "🏨"), unsafe_allow_html=True)
    
    with col4:
        st.markdown(create_elegant_metric_card("RevPAR", f"R$ {kpis['revpar']:,.0f}", kpis['revpar_change'], "🎯"), unsafe_allow_html=True)
    
    # Gráficos principais
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="elegant-section">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Evolução Temporal</div>', unsafe_allow_html=True)
        revenue_chart = create_revenue_evolution_chart(df)
        st.plotly_chart(revenue_chart, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="elegant-section">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Performance</div>', unsafe_allow_html=True)
        property_chart = create_property_performance_chart(df)
        st.plotly_chart(property_chart, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Alertas executivos
    st.markdown('<div class="elegant-section">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Alertas Executivos</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if kpis['revenue_change'] > 15:
            st.markdown(f"""
            <div class="alert-premium success">
                <div class="alert-title">🎉 Meta Superada</div>
                <p>Receita cresceu {kpis['revenue_change']:.1f}% vs mês anterior</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        if kpis['occupancy'] < 70:
            st.markdown(f"""
            <div class="alert-premium warning">
                <div class="alert-title">⚠️ Ocupação Baixa</div>
                <p>Taxa de ocupação em {kpis['occupancy']:.1f}%</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col3:
        total_promo_roi = ((promos['revenue_impact'].sum() - promos['discount_given'].sum()) / promos['discount_given'].sum()) * 100
        st.markdown(f"""
        <div class="alert-premium success">
            <div class="alert-title">💎 ROI Promoções</div>
            <p>Retorno de {total_promo_roi:.0f}% nas campanhas</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_operational_dashboard(df, properties):
    """Dashboard Operacional - Reservas em Tempo Real"""
    st.markdown("## 🏨 Dashboard Operacional")
    
    # Filtros específicos
    col1, col2, col3 = st.columns(3)
    
    with col1:
        status_filter = st.multiselect(
            "Status das Reservas",
            options=df['status'].unique(),
            default=df['status'].unique()
        )
    
    with col2:
        today_only = st.checkbox("Apenas Hoje", value=True)
    
    with col3:
        urgent_only = st.checkbox("Apenas Urgentes")
    
    # Filtrar dados
    ops_df = df[df['status'].isin(status_filter)]
    if today_only:
        ops_df = ops_df[ops_df['check_in'].dt.date == datetime.now().date()]
    
    if urgent_only:
        ops_df = ops_df[ops_df['status'].isin(['pending', 'canceled'])]
    
    # Cards de status em tempo real
    st.markdown("### 📊 Status em Tempo Real")
    
    col1, col2, col3, col4 = st.columns(4)
    
    status_counts = df['status'].value_counts()
    
    with col1:
        confirmed_count = status_counts.get('confirmed', 0)
        st.markdown(create_elegant_metric_card("Confirmadas", str(confirmed_count), 12.5, "✅"), unsafe_allow_html=True)
    
    with col2:
        pending_count = status_counts.get('pending', 0)
        st.markdown(create_elegant_metric_card("Pendentes", str(pending_count), -5.2, "⏳"), unsafe_allow_html=True)
    
    with col3:
        checkin_count = status_counts.get('checked_in', 0)
        st.markdown(create_elegant_metric_card("Check-ins", str(checkin_count), 8.1, "🔑"), unsafe_allow_html=True)
    
    with col4:
        canceled_count = status_counts.get('canceled', 0)
        st.markdown(create_elegant_metric_card("Canceladas", str(canceled_count), -15.3, "❌"), unsafe_allow_html=True)
    
    # Timeline de hoje
    st.markdown("### 📅 Timeline de Hoje")
    
    today_bookings = df[df['check_in'].dt.date == datetime.now().date()].sort_values('check_in')
    
    if not today_bookings.empty:
        for _, booking in today_bookings.head(10).iterrows():
            status_class = f"status-{booking['status']}"
            
            st.markdown(f"""
            <div class="status-card {status_class}">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong>{booking['property_name']}</strong><br>
                        <small>{booking['client_name']} • {booking['guests']} hóspedes</small>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-weight: bold;">R$ {booking['total_price']:,.0f}</div>
                        <div style="font-size: 0.8rem; color: #666;">{booking['check_in'].strftime('%H:%M')}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("📭 Nenhuma reserva para hoje")
    
    # Ações rápidas
    st.markdown("### ⚡ Ações Rápidas")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Atualizar Status", help="Sincronizar com API"):
            st.success("Status atualizados!")
    
    with col2:
        if st.button("📱 Notificar Equipe", help="Enviar alertas"):
            st.success("Equipe notificada!")
    
    with col3:
        if st.button("📊 Relatório do Dia", help="Gerar relatório"):
            st.success("Relatório gerado!")

def render_financial_analytics(df, kpis):
    """Analytics Financeiro Detalhado"""
    st.markdown("## 💰 Analytics Financeiro")
    
    # Métricas financeiras avançadas
    col1, col2, col3, col4, col5 = st.columns(5)
    
    total_revenue = df['total_price'].sum()
    avg_booking_value = df['total_price'].mean()
    
    with col1:
        st.markdown(create_elegant_metric_card("Receita Total", f"R$ {total_revenue:,.0f}", 15.3, "💎"), unsafe_allow_html=True)
    
    with col2:
        st.markdown(create_elegant_metric_card("Ticket Médio", f"R$ {avg_booking_value:,.0f}", 8.7, "🎫"), unsafe_allow_html=True)
    
    with col3:
        weekend_revenue = df[df['check_in'].dt.weekday >= 5]['total_price'].sum()
        weekend_pct = (weekend_revenue / total_revenue) * 100
        st.markdown(create_elegant_metric_card("Rev. Fim de Semana", f"{weekend_pct:.1f}%", 12.1, "🎉"), unsafe_allow_html=True)
    
    with col4:
        vip_revenue = df[df['client_vip'].isin(['Gold', 'Silver'])]['total_price'].sum()
        vip_pct = (vip_revenue / total_revenue) * 100
        st.markdown(create_elegant_metric_card("Receita VIP", f"{vip_pct:.1f}%", 25.4, "👑"), unsafe_allow_html=True)
    
    with col5:
        direct_revenue = df[df['source'] == 'Direct']['total_price'].sum()
        direct_pct = (direct_revenue / total_revenue) * 100
        st.markdown(create_elegant_metric_card("Receita Direta", f"{direct_pct:.1f}%", 18.9, "🎯"), unsafe_allow_html=True)
    
    # Análise por canal
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 Receita por Canal")
        source_revenue = df.groupby('source')['total_price'].sum().sort_values(ascending=False)
        
        fig_source = px.pie(
            values=source_revenue.values,
            names=source_revenue.index,
            title="Distribuição da Receita por Canal",
            color_discrete_sequence=['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe', '#00f2fe']
        )
        fig_source.update_layout(font=dict(family="Inter"))
        st.plotly_chart(fig_source, use_container_width=True)
    
    with col2:
        st.markdown("### 💳 Receita por Método de Pagamento")
        payment_revenue = df.groupby('payment_method')['total_price'].sum().sort_values(ascending=False)
        
        fig_payment = px.bar(
            x=payment_revenue.values,
            y=payment_revenue.index,
            orientation='h',
            title="Receita por Método de Pagamento",
            color=payment_revenue.values,
            color_continuous_scale=[[0, '#667eea'], [1, '#764ba2']]
        )
        fig_payment.update_layout(font=dict(family="Inter"), showlegend=False)
        st.plotly_chart(fig_payment, use_container_width=True)
    
    # Análise temporal detalhada
    st.markdown("### 📊 Análise Temporal Avançada")
    
    tab1, tab2, tab3 = st.tabs(["📅 Por Dia da Semana", "📆 Por Mês", "🕒 Por Hora de Booking"])
    
    with tab1:
        df['weekday'] = df['check_in'].dt.day_name()
        weekday_stats = df.groupby('weekday').agg({
            'total_price': 'sum',
            'daily_rate': 'mean',
            'id': 'count'
        })
        
        fig_weekday = px.bar(
            x=['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom'],
            y=weekday_stats['total_price'].values,
            title="Receita por Dia da Semana",
            color=weekday_stats['total_price'].values,
            color_continuous_scale=[[0, '#667eea'], [1, '#764ba2']]
        )
        fig_weekday.update_layout(font=dict(family="Inter"), showlegend=False)
        st.plotly_chart(fig_weekday, use_container_width=True)
    
    with tab2:
        monthly_revenue = create_revenue_evolution_chart(df)
        st.plotly_chart(monthly_revenue, use_container_width=True)
    
    with tab3:
        df['booking_hour'] = df['booking_date'].dt.hour
        hourly_bookings = df.groupby('booking_hour').size()
        
        fig_hourly = px.line(
            x=hourly_bookings.index,
            y=hourly_bookings.values,
            title="Padrão de Reservas por Hora",
            markers=True
        )
        fig_hourly.update_traces(line_color='#667eea', line_width=3)
        fig_hourly.update_layout(font=dict(family="Inter"))
        st.plotly_chart(fig_hourly, use_container_width=True)

def render_property_central(df, properties):
    """Central de Propriedades - Gestão Completa"""
    st.markdown("## 📋 Central de Propriedades")
    
    # Grid de propriedades
    st.markdown("### 🏨 Status das Propriedades")
    
    property_stats = df.groupby('property_name').agg({
        'total_price': 'sum',
        'daily_rate': 'mean',
        'id': 'count',
        'nights': 'sum'
    }).reset_index()
    
    property_stats['occupancy_rate'] = property_stats['id'] / property_stats['id'].max()
    
    # Cards de propriedades em grid
    cols = st.columns(2)
    
    for idx, (_, prop) in enumerate(property_stats.iterrows()):
        col_idx = idx % 2
        
        performance_class = "high-performance" if prop['occupancy_rate'] > 0.7 else "medium-performance" if prop['occupancy_rate'] > 0.4 else "low-performance"
        performance_color = "#10b981" if prop['occupancy_rate'] > 0.7 else "#f59e0b" if prop['occupancy_rate'] > 0.4 else "#ef4444"
        
        cols[col_idx].markdown(f"""
        <div class="property-card-premium {performance_class}">
            <div class="property-name">{prop['property_name']}</div>
            <div class="property-metrics">
                <div>
                    <div class="property-occupancy" style="color: {performance_color}">
                        {prop['occupancy_rate']:.1%}
                    </div>
                    <div style="font-size: 0.8rem; color: #64748b;">Taxa de Ocupação</div>
                </div>
                <div class="property-details">
                    <div><strong>R$ {prop['total_price']:,.0f}</strong></div>
                    <div>{prop['id']} reservas</div>
                    <div>ADR: R$ {prop['daily_rate']:,.0f}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Calendário de ocupação
    st.markdown("### 📅 Calendário de Ocupação")
    occupancy_heatmap = create_occupancy_heatmap_fixed(df)
    st.plotly_chart(occupancy_heatmap, use_container_width=True)
    
    # Manutenções e bloqueios
    st.markdown("### 🔧 Gestão de Manutenções")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("⚠️ Agendar Manutenção"):
            st.success("Manutenção agendada!")
    
    with col2:
        if st.button("🚫 Bloquear Período"):
            st.success("Período bloqueado!")
    
    with col3:
        if st.button("📊 Relatório de Ocupação"):
            st.success("Relatório gerado!")

def render_promo_codes_dashboard(promos, bookings_df):
    """Dashboard de Códigos Promocionais"""
    st.markdown("## 🎁 Gestão de Códigos Promocionais")
    
    # Métricas de promoções
    col1, col2, col3, col4 = st.columns(4)
    
    total_revenue_impact = promos['revenue_impact'].sum()
    total_discount = promos['discount_given'].sum()
    roi = ((total_revenue_impact - total_discount) / total_discount) * 100
    active_codes = len(promos[promos['active'] == True])
    
    with col1:
        st.markdown(create_elegant_metric_card("Receita Adicional", f"R$ {total_revenue_impact:,.0f}", 22.3, "💎"), unsafe_allow_html=True)
    
    with col2:
        st.markdown(create_elegant_metric_card("Desconto Total", f"R$ {total_discount:,.0f}", -8.7, "🎁"), unsafe_allow_html=True)
    
    with col3:
        st.markdown(create_elegant_metric_card("ROI Médio", f"{roi:.1f}%", 34.5, "📈"), unsafe_allow_html=True)
    
    with col4:
        st.markdown(create_elegant_metric_card("Códigos Ativos", str(active_codes), 15.0, "🔥"), unsafe_allow_html=True)
    
    # Tabela de códigos
    st.markdown("### 📋 Códigos Promocionais Ativos")
    
    promo_display = promos.copy()
    promo_display['ROI'] = ((promo_display['revenue_impact'] - promo_display['discount_given']) / promo_display['discount_given'] * 100).round(1)
    promo_display['Usage%'] = (promo_display['uses'] / promo_display['max_uses'] * 100).round(1)
    promo_display['Status'] = promo_display['active'].map({True: '🟢 Ativo', False: '🔴 Inativo'})
    
    st.dataframe(
        promo_display[['code', 'discount', 'type', 'uses', 'max_uses', 'Usage%', 'ROI', 'Status']].rename(columns={
            'code': 'Código',
            'discount': 'Desconto',
            'type': 'Tipo',
            'uses': 'Usos',
            'max_uses': 'Máx Usos',
            'Usage%': 'Uso %',
            'Status': 'Status'
        }),
        use_container_width=True,
        hide_index=True
    )
    
    # Performance por código
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Performance por Código")
        fig_promo_perf = px.bar(
            promo_display,
            x='code',
            y='revenue_impact',
            title="Receita Adicional por Código",
            color='revenue_impact',
            color_continuous_scale=[[0, '#667eea'], [1, '#764ba2']]
        )
        fig_promo_perf.update_layout(font=dict(family="Inter"), showlegend=False)
        st.plotly_chart(fig_promo_perf, use_container_width=True)
    
    with col2:
        st.markdown("### 🎯 Taxa de Uso")
        fig_usage = px.bar(
            promo_display,
            x='code',
            y='Usage%',
            title="Taxa de Utilização (%)",
            color='Usage%',
            color_continuous_scale=[[0, '#f59e0b'], [1, '#10b981']]
        )
        fig_usage.update_layout(font=dict(family="Inter"), showlegend=False)
        st.plotly_chart(fig_usage, use_container_width=True)
    
    # Criação de novo código
    st.markdown("### ➕ Criar Novo Código")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        new_code = st.text_input("Código", placeholder="Ex: VERAO2025")
        discount_type = st.selectbox("Tipo", ["percent", "fixed"])
        discount_value = st.number_input("Valor do Desconto", min_value=1, value=15)
    
    with col2:
        max_uses = st.number_input("Máximo de Usos", min_value=1, value=100)
        start_date = st.date_input("Data Início", value=datetime.now().date())
        end_date = st.date_input("Data Fim", value=datetime.now().date() + timedelta(days=30))
    
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🎁 Criar Código Promocional", type="primary"):
            st.balloons()
            st.success(f"Código {new_code} criado com sucesso!")

def render_customer_analytics(df, clients):
    """Análise de Clientes Detalhada"""
    st.markdown("## 👥 Análise de Clientes")
    
    # Métricas de clientes
    col1, col2, col3, col4 = st.columns(4)
    
    unique_clients = df['client_id'].nunique()
    vip_clients = df[df['client_vip'].isin(['Gold', 'Silver'])]['client_id'].nunique()
    repeat_rate = (df.groupby('client_id').size() > 1).mean() * 100
    avg_ltv = df.groupby('client_id')['total_price'].sum().mean()
    
    with col1:
        st.markdown(create_elegant_metric_card("Clientes Únicos", str(unique_clients), 8.5, "👥"), unsafe_allow_html=True)
    
    with col2:
        st.markdown(create_elegant_metric_card("Clientes VIP", str(vip_clients), 15.2, "👑"), unsafe_allow_html=True)
    
    with col3:
        st.markdown(create_elegant_metric_card("Taxa de Retorno", f"{repeat_rate:.1f}%", 12.8, "🔄"), unsafe_allow_html=True)
    
    with col4:
        st.markdown(create_elegant_metric_card("LTV Médio", f"R$ {avg_ltv:,.0f}", 18.3, "💎"), unsafe_allow_html=True)
    
    # Análise por segmento
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🌍 Clientes por País")
        country_stats = df['client_country'].value_counts()
        fig_country = px.pie(
            values=country_stats.values,
            names=country_stats.index,
            title="Distribuição por País",
            color_discrete_sequence=['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe']
        )
        fig_country.update_layout(font=dict(family="Inter"))
        st.plotly_chart(fig_country, use_container_width=True)
    
    with col2:
        st.markdown("### 👑 Segmentação VIP")
        vip_stats = df['client_vip'].value_counts()
        fig_vip = px.bar(
            x=vip_stats.index,
            y=vip_stats.values,
            title="Clientes por Segmento",
            color=vip_stats.values,
            color_continuous_scale=[[0, '#667eea'], [1, '#764ba2']]
        )
        fig_vip.update_layout(font=dict(family="Inter"), showlegend=False)
        st.plotly_chart(fig_vip, use_container_width=True)
    
    # Top clientes
    st.markdown("### 🏆 Top Clientes por Receita")
    
    top_clients = df.groupby(['client_id', 'client_name', 'client_vip']).agg({
        'total_price': 'sum',
        'id': 'count',
        'nights': 'sum'
    }).reset_index().sort_values('total_price', ascending=False).head(10)
    
    for _, client in top_clients.iterrows():
        vip_badge = {"Gold": "🥇", "Silver": "🥈", "Bronze": "🥉", "Regular": "⭐"}.get(client['client_vip'], "⭐")
        
        st.markdown(f"""
        <div class="property-card-premium">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <strong>{vip_badge} {client['client_name']}</strong><br>
                    <small>Status: {client['client_vip']} • {client['id']} reservas • {client['nights']} noites</small>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 1.4rem; font-weight: bold; color: #667eea;">R$ {client['total_price']:,.0f}</div>
                    <div style="font-size: 0.9rem; color: #666;">Lifetime Value</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def render_business_intelligence(df, kpis):
    """Business Intelligence Avançado"""
    st.markdown("## 🔍 Business Intelligence")
    
    # Insights automáticos
    st.markdown("### 💡 Insights Automáticos")
    
    # Análise de sazonalidade
    df['month'] = df['check_in'].dt.month
    seasonal_revenue = df.groupby('month')['total_price'].sum()
    peak_month = seasonal_revenue.idxmax()
    low_month = seasonal_revenue.idxmin()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="alert-premium success">
            <div class="alert-title">📈 Sazonalidade</div>
            <p>Mês {peak_month} é o mais lucrativo com R$ {seasonal_revenue[peak_month]:,.0f}</p>
            <p><strong>Recomendação:</strong> Aumentar preços em 20% no período de alta</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        weekend_vs_weekday = df.groupby(df['check_in'].dt.weekday >= 5)['total_price'].sum()
        weekend_premium = (weekend_vs_weekday[True] / weekend_vs_weekday[False] - 1) * 100
        
        st.markdown(f"""
        <div class="alert-premium warning">
            <div class="alert-title">🎉 Fins de Semana</div>
            <p>Receita {weekend_premium:.0f}% maior em fins de semana</p>
            <p><strong>Oportunidade:</strong> Dynamic pricing para maximize receita</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        cancellation_rate = (len(df[df['status'] == 'canceled']) / len(df)) * 100
        st.markdown(f"""
        <div class="alert-premium {'success' if cancellation_rate < 5 else 'warning'}">
            <div class="alert-title">❌ Taxa de Cancelamento</div>
            <p>Taxa atual: {cancellation_rate:.1f}%</p>
            <p><strong>Status:</strong> {'Excelente' if cancellation_rate < 5 else 'Atenção necessária'}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Previsões e projeções
    st.markdown("### 📊 Projeções e Tendências")
    
    tab1, tab2, tab3 = st.tabs(["📈 Previsão Receita", "🎯 Oportunidades", "⚠️ Riscos"])
    
    with tab1:
        # Simulação de previsão baseada em tendência
        monthly_revenue = df.groupby(df['check_in'].dt.to_period('M'))['total_price'].sum()
        growth_rate = (monthly_revenue.iloc[-1] / monthly_revenue.iloc[-2] - 1) if len(monthly_revenue) > 1 else 0.1
        
        projected_revenue = monthly_revenue.iloc[-1] * (1 + growth_rate)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Receita Projetada Próximo Mês", f"R$ {projected_revenue:,.0f}", f"{growth_rate*100:.1f}%")
        
        with col2:
            st.metric("Receita Projetada Anual", f"R$ {projected_revenue * 12:,.0f}", f"Base: crescimento atual")
    
    with tab2:
        st.markdown("#### 🚀 Oportunidades Identificadas")
        
        opportunities = [
            "Implementar dynamic pricing pode aumentar receita em 25%",
            "Foco em clientes VIP pode elevar LTV em 40%",
            "Expansão para região de menor ocupação com potencial de 30% crescimento",
            "Programa de fidelidade pode reduzir cancelamentos em 15%",
            "Upselling de serviços adicionais com margem de 60%"
        ]
        
        for opp in opportunities:
            st.success(f"💡 {opp}")
    
    with tab3:
        st.markdown("#### ⚠️ Riscos Monitorados")
        
        risks = [
            "Dependência excessiva de canais externos (65% da receita)",
            "Sazonalidade alta pode impactar fluxo de caixa",
            "Taxa de ocupação baixa em propriedades específicas",
            "Concentração geográfica em 2 regiões apenas",
            "Clientes não-recorrentes representam 70% da base"
        ]
        
        for risk in risks:
            st.warning(f"⚠️ {risk}")
    
    # Relatórios executivos
    st.markdown("### 📋 Ações Recomendadas")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Gerar Relatório Executivo", type="primary"):
            st.balloons()
            st.success("Relatório executivo gerado e enviado!")
    
    with col2:
        if st.button("📈 Análise Preditiva"):
            st.success("Análise preditiva iniciada!")
    
    with col3:
        if st.button("🎯 Plano de Ação"):
            st.success("Plano de ação estratégico criado!")

if __name__ == "__main__":
    main()
