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
    page_title="Stays Analytics | Premium Dashboard",
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
    
    /* Botões premium */
    .btn-premium {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 1rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .btn-premium:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
    }
    
    /* Tabs elegantes */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
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
    
    /* Dataframe elegante */
    .dataframe {
        border: none !important;
        border-radius: 12px !important;
        overflow: hidden !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05) !important;
    }
    
    /* Loading spinner */
    .stSpinner {
        text-align: center;
    }
    
    /* Métricas responsivas */
    @media (max-width: 768px) {
        .elegant-header h1 {
            font-size: 2.5rem;
        }
        
        .metric-value {
            font-size: 2.2rem;
        }
        
        .premium-metric-card {
            padding: 2rem 1.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Funções de dados (mantendo a mesma lógica, mas melhorando a apresentação)
@st.cache_data(ttl=300)
def generate_stays_demo_data():
    """Gera dados realistas baseados na API Stays"""
    fake = Faker('pt_PT')
    np.random.seed(42)
    
    # Dados de propriedades premium
    properties = [
        {"id": "LU01F", "name": "Vibe República Premium", "type": "entire_place", "region": "São Paulo", "city": "São Paulo"},
        {"id": "CP02A", "name": "Copacabana Luxury Suite", "type": "entire_place", "region": "Rio de Janeiro", "city": "Rio de Janeiro"},
        {"id": "IP03B", "name": "Ipanema Ocean View", "type": "private_room", "region": "Rio de Janeiro", "city": "Rio de Janeiro"},
        {"id": "CE04C", "name": "Centro Business Hub", "type": "entire_place", "region": "São Paulo", "city": "São Paulo"},
        {"id": "VM05D", "name": "Vila Madalena Loft", "type": "entire_place", "region": "São Paulo", "city": "São Paulo"},
        {"id": "LE06E", "name": "Leblon Beachfront", "type": "private_room", "region": "Rio de Janeiro", "city": "Rio de Janeiro"},
        {"id": "PI07F", "name": "Pinheiros Modern", "type": "entire_place", "region": "São Paulo", "city": "São Paulo"},
        {"id": "BO08G", "name": "Botafogo Panoramic", "type": "private_room", "region": "Rio de Janeiro", "city": "Rio de Janeiro"},
    ]
    
    # Gerar dados de reservas dos últimos 6 meses
    bookings = []
    start_date = datetime.now() - timedelta(days=180)
    
    for i in range(520):
        property_data = np.random.choice(properties)
        check_in = start_date + timedelta(days=np.random.randint(0, 180))
        stay_duration = np.random.randint(1, 10)
        check_out = check_in + timedelta(days=stay_duration)
        
        # Preços premium baseados na região e tipo
        base_prices = {
            ("Rio de Janeiro", "entire_place"): 420,
            ("Rio de Janeiro", "private_room"): 220,
            ("São Paulo", "entire_place"): 340,
            ("São Paulo", "private_room"): 180
        }
        
        base_price = base_prices.get((property_data["region"], property_data["type"]), 250)
        
        # Variação sazonal e fins de semana
        seasonal_factor = 1.3 if check_in.month in [12, 1, 2, 6, 7] else 1.0
        weekend_factor = 1.4 if check_in.weekday() >= 5 else 1.0
        price_variation = np.random.uniform(0.85, 1.6)
        
        total_price = base_price * stay_duration * seasonal_factor * weekend_factor * price_variation
        
        booking = {
            "id": f"RES{i+1:03d}",
            "property_id": property_data["id"],
            "property_name": property_data["name"],
            "property_type": property_data["type"],
            "region": property_data["region"],
            "city": property_data["city"],
            "check_in": check_in,
            "check_out": check_out,
            "guests": np.random.randint(1, 6),
            "nights": stay_duration,
            "total_price": round(total_price, 2),
            "daily_rate": round(total_price / stay_duration, 2),
            "status": np.random.choice(["confirmed", "pending", "canceled"], p=[0.88, 0.09, 0.03]),
            "guest_name": fake.name(),
            "guest_email": fake.email(),
            "booking_date": check_in - timedelta(days=np.random.randint(1, 45)),
            "source": np.random.choice(["Direct", "Booking.com", "Airbnb", "Expedia"], p=[0.35, 0.35, 0.2, 0.1])
        }
        bookings.append(booking)
    
    return pd.DataFrame(bookings), properties

@st.cache_data(ttl=300)
def generate_promo_codes_data():
    """Simula dados de códigos promocionais premium"""
    promo_codes = [
        {"code": "PREMIUM25", "discount": 25, "type": "percent", "uses": 189, "max_uses": 250, "revenue_impact": 125400, "discount_given": 31350},
        {"code": "EXECUTIVO15", "discount": 15, "type": "percent", "uses": 134, "max_uses": 200, "revenue_impact": 78900, "discount_given": 18200},
        {"code": "NEGOCIOS", "discount": 30, "type": "percent", "uses": 97, "max_uses": 150, "revenue_impact": 56300, "discount_given": 24100},
        {"code": "FIDELIDADE", "discount": 100, "type": "fixed", "uses": 67, "max_uses": 100, "revenue_impact": 34200, "discount_given": 6700},
        {"code": "TEMPORADA", "discount": 20, "type": "percent", "uses": 203, "max_uses": 400, "revenue_impact": 98600, "discount_given": 24650}
    ]
    return pd.DataFrame(promo_codes)

def calculate_kpis(df):
    """Calcula KPIs principais com melhor precisão"""
    current_month = datetime.now().replace(day=1)
    last_month = (current_month - timedelta(days=1)).replace(day=1)
    
    current_data = df[df['check_in'] >= current_month]
    last_month_data = df[(df['check_in'] >= last_month) & (df['check_in'] < current_month)]
    
    kpis = {}
    
    # Receita total
    kpis['revenue'] = current_data['total_price'].sum()
    kpis['revenue_last'] = last_month_data['total_price'].sum()
    kpis['revenue_change'] = ((kpis['revenue'] - kpis['revenue_last']) / kpis['revenue_last']) * 100 if kpis['revenue_last'] > 0 else 0
    
    # ADR (Average Daily Rate)
    kpis['adr'] = current_data['daily_rate'].mean() if not current_data.empty else 0
    kpis['adr_last'] = last_month_data['daily_rate'].mean() if not last_month_data.empty else 0
    kpis['adr_change'] = ((kpis['adr'] - kpis['adr_last']) / kpis['adr_last']) * 100 if kpis['adr_last'] > 0 else 0
    
    # Reservas
    kpis['bookings'] = len(current_data)
    kpis['bookings_last'] = len(last_month_data)
    kpis['bookings_change'] = ((kpis['bookings'] - kpis['bookings_last']) / kpis['bookings_last']) * 100 if kpis['bookings_last'] > 0 else 0
    
    # RevPAR simplificado
    total_properties = 8
    days_in_month = datetime.now().day
    kpis['revpar'] = kpis['revenue'] / (total_properties * days_in_month) if days_in_month > 0 else 0
    
    last_month_days = (current_month - timedelta(days=1)).day
    kpis['revpar_last'] = kpis['revenue_last'] / (total_properties * last_month_days) if last_month_days > 0 else 0
    kpis['revpar_change'] = ((kpis['revpar'] - kpis['revpar_last']) / kpis['revpar_last']) * 100 if kpis['revpar_last'] > 0 else 0
    
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

def create_revenue_chart_elegant(df):
    """Cria gráfico de receita elegante"""
    df['month'] = df['check_in'].dt.to_period('M')
    monthly_data = df.groupby('month').agg({
        'total_price': 'sum',
        'id': 'count',
        'daily_rate': 'mean'
    }).reset_index()
    
    monthly_data['month_str'] = monthly_data['month'].astype(str)
    
    fig = go.Figure()
    
    # Linha principal com gradiente
    fig.add_trace(go.Scatter(
        x=monthly_data['month_str'],
        y=monthly_data['total_price'],
        mode='lines+markers',
        name='Receita Mensal',
        line=dict(
            color='rgba(102, 126, 234, 1)',
            width=4,
            shape='spline'
        ),
        marker=dict(
            size=12,
            color='rgba(102, 126, 234, 1)',
            line=dict(color='white', width=3)
        ),
        fill='tonexty',
        fillcolor='rgba(102, 126, 234, 0.1)',
        hovertemplate='<b>%{x}</b><br>Receita: R$ %{y:,.0f}<extra></extra>'
    ))
    
    fig.update_layout(
        title={
            'text': '<b>Evolução da Receita Mensal</b>',
            'font': {'size': 24, 'family': 'Inter'},
            'x': 0.02
        },
        xaxis_title="Período",
        yaxis_title="Receita (R$)",
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter", size=14),
        hovermode='x unified',
        showlegend=False,
        margin=dict(l=20, r=20, t=60, b=20)
    )
    
    fig.update_xaxes(
        gridcolor='rgba(0,0,0,0.05)',
        showgrid=True,
        zeroline=False
    )
    
    fig.update_yaxes(
        gridcolor='rgba(0,0,0,0.05)',
        showgrid=True,
        zeroline=False,
        tickformat=',.0f'
    )
    
    return fig

def create_property_performance_elegant(df):
    """Cria gráfico de performance por propriedade elegante"""
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
        textfont=dict(color='white', size=12, family='Inter'),
        hovertemplate='<b>%{y}</b><br>Receita: R$ %{x:,.0f}<extra></extra>'
    ))
    
    fig.update_layout(
        title={
            'text': '<b>Performance por Propriedade</b>',
            'font': {'size': 20, 'family': 'Inter'},
            'x': 0.02
        },
        xaxis_title="Receita Total (R$)",
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter", size=12),
        margin=dict(l=20, r=20, t=50, b=20)
    )
    
    fig.update_xaxes(
        gridcolor='rgba(0,0,0,0.05)',
        showgrid=True,
        zeroline=False,
        tickformat=',.0f'
    )
    
    fig.update_yaxes(
        gridcolor='rgba(0,0,0,0.05)',
        showgrid=False
    )
    
    return fig

def create_occupancy_heatmap_elegant(df):
    """Cria mapa de calor elegante"""
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
        colorbar=dict(
            title="Reservas",
            titlefont=dict(family="Inter")
        ),
        hoverongaps=False,
        hovertemplate='Semana %{y}<br>%{x}: %{z} reservas<extra></extra>'
    ))
    
    fig.update_layout(
        title={
            'text': '<b>Padrão de Ocupação Semanal</b>',
            'font': {'size': 20, 'family': 'Inter'},
            'x': 0.02
        },
        xaxis_title="Dia da Semana",
        yaxis_title="Semana do Ano",
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter", size=12),
        margin=dict(l=20, r=20, t=50, b=20)
    )
    
    return fig

# Interface principal elegante
def main():
    # Header elegante com animação
    st.markdown("""
    <div class="elegant-header">
        <h1>Stays Analytics</h1>
        <p>Dashboard Premium para Gestão Hoteleira Inteligente</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Carregamento elegante
    with st.spinner('🚀 Carregando insights premium...'):
        df_bookings, properties = generate_stays_demo_data()
        df_promos = generate_promo_codes_data()
        time.sleep(0.5)  # Efeito visual
    
    # Sidebar elegante
    with st.sidebar:
        st.markdown('<div class="filter-container">', unsafe_allow_html=True)
        st.markdown('<div class="filter-title">🎯 Filtros Inteligentes</div>', unsafe_allow_html=True)
        
        date_range = st.date_input(
            "📅 Período de Análise",
            value=[datetime.now() - timedelta(days=30), datetime.now()],
            max_value=datetime.now(),
            help="Selecione o período para análise detalhada"
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="filter-container">', unsafe_allow_html=True)
        st.markdown('<div class="filter-title">🏙️ Segmentação</div>', unsafe_allow_html=True)
        
        regions = st.multiselect(
            "Regiões",
            options=df_bookings['region'].unique(),
            default=df_bookings['region'].unique()
        )
        
        property_types = st.multiselect(
            "Tipos de Propriedade",
            options=df_bookings['property_type'].unique(),
            default=df_bookings['property_type'].unique()
        )
        
        status_filter = st.multiselect(
            "Status das Reservas",
            options=df_bookings['status'].unique(),
            default=['confirmed']
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Insights rápidos na sidebar
        st.markdown('<div class="filter-container">', unsafe_allow_html=True)
        st.markdown('<div class="filter-title">💡 Insight Rápido</div>', unsafe_allow_html=True)
        
        best_property = df_bookings.groupby('property_name')['total_price'].sum().idxmax()
        best_revenue = df_bookings.groupby('property_name')['total_price'].sum().max()
        
        st.markdown(f"""
        <div style="text-align: center; padding: 1rem;">
            <div style="font-size: 0.9rem; color: #64748b; margin-bottom: 0.5rem;">🏆 Top Property</div>
            <div style="font-weight: 700; color: #1e293b; margin-bottom: 0.3rem;">{best_property}</div>
            <div style="font-size: 1.2rem; font-weight: 800; color: #667eea;">R$ {best_revenue:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Filtrar dados
    filtered_df = df_bookings[
        (df_bookings['check_in'] >= pd.to_datetime(date_range[0])) &
        (df_bookings['check_in'] <= pd.to_datetime(date_range[1])) &
        (df_bookings['region'].isin(regions)) &
        (df_bookings['property_type'].isin(property_types)) &
        (df_bookings['status'].isin(status_filter))
    ]
    
    # Calcular KPIs
    kpis = calculate_kpis(df_bookings)
    
    # Métricas principais em cards elegantes
    st.markdown("## 📈 Indicadores Principais")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(
            create_elegant_metric_card(
                "Receita Total",
                f"R$ {kpis['revenue']:,.0f}",
                kpis['revenue_change'],
                "💰"
            ),
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            create_elegant_metric_card(
                "ADR Médio",
                f"R$ {kpis['adr']:,.0f}",
                kpis['adr_change'],
                "📊"
            ),
            unsafe_allow_html=True
        )
    
    with col3:
        st.markdown(
            create_elegant_metric_card(
                "Reservas",
                f"{kpis['bookings']:,}",
                kpis['bookings_change'],
                "📋"
            ),
            unsafe_allow_html=True
        )
    
    with col4:
        st.markdown(
            create_elegant_metric_card(
                "RevPAR",
                f"R$ {kpis['revpar']:,.0f}",
                kpis['revpar_change'],
                "🎯"
            ),
            unsafe_allow_html=True
        )
    
    # Seção de análise visual
    st.markdown('<div class="elegant-section">', unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="section-title">Análise Temporal</div>', unsafe_allow_html=True)
        revenue_chart = create_revenue_chart_elegant(filtered_df)
        st.plotly_chart(revenue_chart, use_container_width=True, key="revenue_chart")
    
    with col2:
        st.markdown('<div class="section-title">Top Properties</div>', unsafe_allow_html=True)
        property_chart = create_property_performance_elegant(filtered_df)
        st.plotly_chart(property_chart, use_container_width=True, key="property_chart")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Análise detalhada em tabs elegantes
    st.markdown('<div class="elegant-section">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Análise Avançada</div>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["📅 Padrões de Ocupação", "🎁 Códigos Promocionais", "📊 Reservas Detalhadas", "💡 Insights Estratégicos"])
    
    with tab1:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            heatmap_chart = create_occupancy_heatmap_elegant(filtered_df)
            st.plotly_chart(heatmap_chart, use_container_width=True)
        
        with col2:
            st.markdown("### 🏢 Status das Propriedades")
            
            # Cards de propriedade elegantes
            property_performance = filtered_df.groupby('property_name').agg({
                'total_price': 'sum',
                'id': 'count'
            }).reset_index()
            
            property_performance['occupancy'] = property_performance['id'] / property_performance['id'].max()
            
            for _, prop in property_performance.head(6).iterrows():
                performance_class = "high-performance" if prop['occupancy'] > 0.7 else "medium-performance" if prop['occupancy'] > 0.4 else "low-performance"
                
                st.markdown(f"""
                <div class="property-card-premium {performance_class}">
                    <div class="property-name">{prop['property_name']}</div>
                    <div class="property-metrics">
                        <div>
                            <div class="property-occupancy" style="color: {'#10b981' if prop['occupancy'] > 0.7 else '#f59e0b' if prop['occupancy'] > 0.4 else '#ef4444'}">
                                {prop['occupancy']:.1%}
                            </div>
                        </div>
                        <div class="property-details">
                            <div><strong>R$ {prop['total_price']:,.0f}</strong></div>
                            <div>{prop['id']} reservas</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### 🎯 Performance dos Códigos Promocionais")
        
        col1, col2, col3 = st.columns(3)
        
        total_revenue_promo = df_promos['revenue_impact'].sum()
        total_discount = df_promos['discount_given'].sum()
        roi_promo = ((total_revenue_promo - total_discount) / total_discount) * 100
        
        with col1:
            st.markdown(
                create_elegant_metric_card(
                    "Receita Adicional",
                    f"R$ {total_revenue_promo:,.0f}",
                    12.5,
                    "💎"
                ),
                unsafe_allow_html=True
            )
        
        with col2:
            st.markdown(
                create_elegant_metric_card(
                    "Desconto Total",
                    f"R$ {total_discount:,.0f}",
                    -8.2,
                    "🎁"
                ),
                unsafe_allow_html=True
            )
        
        with col3:
            st.markdown(
                create_elegant_metric_card(
                    "ROI Promoções",
                    f"{roi_promo:.1f}%",
                    roi_promo,
                    "📈"
                ),
                unsafe_allow_html=True
            )
        
        # Tabela elegante de promoções
        st.markdown("#### 📋 Detalhamento dos Códigos")
        promo_display = df_promos.copy()
        promo_display['ROI'] = ((promo_display['revenue_impact'] - promo_display['discount_given']) / promo_display['discount_given'] * 100).round(1)
        promo_display['Eficiência'] = (promo_display['uses'] / promo_display['max_uses'] * 100).round(1)
        
        st.dataframe(
            promo_display[['code', 'uses', 'revenue_impact', 'discount_given', 'ROI', 'Eficiência']].rename(columns={
                'code': 'Código',
                'uses': 'Usos',
                'revenue_impact': 'Receita Adicional',
                'discount_given': 'Desconto Dado'
            }),
            use_container_width=True,
            hide_index=True
        )
    
    with tab3:
        st.markdown("### 📊 Análise Detalhada de Reservas")
        
        # Métricas de reservas
        col1, col2 = st.columns(2)
        
        with col1:
            source_stats = filtered_df['source'].value_counts()
            fig_source = px.pie(
                values=source_stats.values,
                names=source_stats.index,
                title="Origem das Reservas",
                color_discrete_sequence=['#667eea', '#764ba2', '#f093fb', '#f5576c']
            )
            fig_source.update_layout(
                font=dict(family="Inter"),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_source, use_container_width=True)
        
        with col2:
            region_stats = filtered_df.groupby('region')['total_price'].sum()
            fig_region = px.bar(
                x=region_stats.index,
                y=region_stats.values,
                title="Receita por Região",
                color=region_stats.values,
                color_continuous_scale=[[0, '#667eea'], [1, '#764ba2']]
            )
            fig_region.update_layout(
                font=dict(family="Inter"),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                showlegend=False
            )
            st.plotly_chart(fig_region, use_container_width=True)
        
        # Tabela de reservas recentes
        st.markdown("#### 📋 Reservas Recentes")
        recent_bookings = filtered_df.sort_values('check_in', ascending=False).head(15)
        
        display_bookings = recent_bookings[['property_name', 'guest_name', 'check_in', 'check_out', 'total_price', 'status']].copy()
        display_bookings['check_in'] = display_bookings['check_in'].dt.strftime('%d/%m/%Y')
        display_bookings['check_out'] = display_bookings['check_out'].dt.strftime('%d/%m/%Y')
        display_bookings.columns = ['Propriedade', 'Hóspede', 'Check-in', 'Check-out', 'Valor Total', 'Status']
        
        st.dataframe(
            display_bookings,
            use_container_width=True,
            hide_index=True
        )
    
    with tab4:
        st.markdown("### 💡 Insights Estratégicos Premium")
        
        # Análise automática avançada
        total_revenue = filtered_df['total_price'].sum()
        best_property = filtered_df.groupby('property_name')['total_price'].sum().idxmax()
        best_region = filtered_df.groupby('region')['total_price'].sum().idxmax()
        avg_stay = filtered_df['nights'].mean()
        weekend_revenue = filtered_df[filtered_df['check_in'].dt.weekday >= 5]['total_price'].sum()
        weekday_revenue = total_revenue - weekend_revenue
        
        # Cards de insights premium
        insights_data = [
            {
                "tipo": "success",
                "icon": "🏆",
                "titulo": "Propriedade Estrela",
                "conteudo": f"{best_property} lidera com {(filtered_df[filtered_df['property_name'] == best_property]['total_price'].sum() / total_revenue * 100):.1f}% da receita total. Modelo de sucesso para replicação.",
                "acao": "Analisar fatores de sucesso para outras propriedades"
            },
            {
                "tipo": "warning",
                "icon": "📍",
                "titulo": "Oportunidade Regional",
                "conteudo": f"{best_region} demonstra potencial superior. Receita de fins de semana é {(weekend_revenue/weekday_revenue*100):.0f}% maior que dias úteis.",
                "acao": "Implementar estratégia de expansão regional"
            },
            {
                "tipo": "info",
                "icon": "📊",
                "titulo": "Padrão de Estadia",
                "conteudo": f"Estadias médias de {avg_stay:.1f} noites indicam perfil de turismo leisure. Oportunidade para pacotes longos.",
                "acao": "Criar promoções para estadias 5+ noites"
            }
        ]
        
        for insight in insights_data:
            st.markdown(f"""
            <div class="alert-premium {insight['tipo']}">
                <div class="alert-title">{insight['icon']} {insight['titulo']}</div>
                <p style="margin-bottom: 0.8rem;">{insight['conteudo']}</p>
                <div style="font-weight: 600; font-size: 0.9rem;">💡 Recomendação: {insight['acao']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Recomendações estratégicas premium
        st.markdown("#### 🚀 Plano de Ação Estratégico")
        
        recommendations = [
            "Implementar dynamic pricing com +25% para fins de semana em propriedades premium",
            "Expandir portfólio em regiões de alta performance (ROI esperado: 35%)",
            "Lançar programa VIP para hóspedes recorrentes com benefícios exclusivos",
            "Otimizar mix de códigos promocionais baseado em análise de elasticidade",
            "Desenvolver parcerias estratégicas para aumento de direct bookings"
        ]
        
        for i, rec in enumerate(recommendations, 1):
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%); 
                        border-left: 4px solid #667eea; padding: 1rem; margin: 0.8rem 0; border-radius: 8px;">
                <div style="font-weight: 700; color: #1e293b; margin-bottom: 0.3rem;">
                    🎯 Ação {i}
                </div>
                <div style="color: #475569;">
                    {rec}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer premium com call-to-action
    st.markdown('<div class="elegant-section">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Próximos Passos</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📈 Relatório Executivo", key="relatorio", help="Gere um relatório completo"):
            st.balloons()
            st.success("🎉 Relatório executivo enviado com sucesso!")
    
    with col2:
        if st.button("🔄 Atualizar Dashboard", key="refresh", help="Atualize os dados"):
            st.cache_data.clear()
            st.success("✨ Dashboard atualizado!")
            st.rerun()
    
    with col3:
        if st.button("📞 Agendar Consultoria", key="consultoria", help="Agende uma reunião estratégica"):
            st.info("📅 Redirecionando para agendamento...")
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
