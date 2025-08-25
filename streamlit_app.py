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
    page_title="Stays Analytics Dashboard",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para design profissional
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #2962ff 0%, #1976d2 100%);
        padding: 2rem 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #2962ff;
        margin: 1rem 0;
    }
    
    .property-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .property-high { border-left-color: #28a745; }
    .property-medium { border-left-color: #ffc107; }
    .property-low { border-left-color: #dc3545; }
    
    .sidebar .sidebar-content {
        background: #f8f9fa;
    }
    
    .alert-card {
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid;
    }
    
    .alert-success { 
        background: #d4edda; 
        border-left-color: #28a745; 
        color: #155724; 
    }
    
    .alert-warning { 
        background: #fff3cd; 
        border-left-color: #ffc107; 
        color: #856404; 
    }
    
    .alert-danger { 
        background: #f8d7da; 
        border-left-color: #dc3545; 
        color: #721c24; 
    }
</style>
""", unsafe_allow_html=True)

# Funções de simulação de dados da API Stays
@st.cache_data(ttl=300)
def generate_stays_demo_data():
    """Gera dados realistas baseados na API Stays"""
    fake = Faker('pt_PT')
    np.random.seed(42)  # Para consistência na demo
    
    # Dados de propriedades
    properties = [
        {"id": "LU01F", "name": "Vibe República", "type": "entire_place", "region": "São Paulo", "city": "São Paulo"},
        {"id": "CP02A", "name": "Copacabana Luxury", "type": "entire_place", "region": "Rio de Janeiro", "city": "Rio de Janeiro"},
        {"id": "IP03B", "name": "Ipanema Suite", "type": "private_room", "region": "Rio de Janeiro", "city": "Rio de Janeiro"},
        {"id": "CE04C", "name": "Centro Business", "type": "entire_place", "region": "São Paulo", "city": "São Paulo"},
        {"id": "VM05D", "name": "Vila Madalena Loft", "type": "entire_place", "region": "São Paulo", "city": "São Paulo"},
        {"id": "LE06E", "name": "Leblon Beachfront", "type": "private_room", "region": "Rio de Janeiro", "city": "Rio de Janeiro"},
        {"id": "PI07F", "name": "Pinheiros Modern", "type": "entire_place", "region": "São Paulo", "city": "São Paulo"},
        {"id": "BO08G", "name": "Botafogo View", "type": "private_room", "region": "Rio de Janeiro", "city": "Rio de Janeiro"},
    ]
    
    # Gerar dados de reservas dos últimos 6 meses
    bookings = []
    start_date = datetime.now() - timedelta(days=180)
    
    for i in range(450):  # ~2.5 reservas por dia
        property_data = np.random.choice(properties)
        check_in = start_date + timedelta(days=np.random.randint(0, 180))
        stay_duration = np.random.randint(1, 8)
        check_out = check_in + timedelta(days=stay_duration)
        
        # Preço baseado na região e tipo
        base_prices = {
            ("Rio de Janeiro", "entire_place"): 350,
            ("Rio de Janeiro", "private_room"): 180,
            ("São Paulo", "entire_place"): 280,
            ("São Paulo", "private_room"): 150
        }
        
        base_price = base_prices.get((property_data["region"], property_data["type"]), 200)
        
        # Variação sazonal e fins de semana
        seasonal_factor = 1.2 if check_in.month in [12, 1, 2, 6, 7] else 1.0
        weekend_factor = 1.3 if check_in.weekday() >= 5 else 1.0
        price_variation = np.random.uniform(0.8, 1.4)
        
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
            "guests": np.random.randint(1, 5),
            "nights": stay_duration,
            "total_price": round(total_price, 2),
            "daily_rate": round(total_price / stay_duration, 2),
            "status": np.random.choice(["confirmed", "pending", "canceled"], p=[0.85, 0.10, 0.05]),
            "guest_name": fake.name(),
            "guest_email": fake.email(),
            "booking_date": check_in - timedelta(days=np.random.randint(1, 30)),
            "source": np.random.choice(["Direct", "Booking.com", "Airbnb", "Expedia"], p=[0.3, 0.4, 0.2, 0.1])
        }
        bookings.append(booking)
    
    return pd.DataFrame(bookings), properties

@st.cache_data(ttl=300)
def generate_promo_codes_data():
    """Simula dados de códigos promocionais"""
    promo_codes = [
        {"code": "VERAO25", "discount": 15, "type": "percent", "uses": 156, "max_uses": 200, "revenue_impact": 89200, "discount_given": 23400},
        {"code": "FAMILIA10", "discount": 10, "type": "percent", "uses": 89, "max_uses": 150, "revenue_impact": 45600, "discount_given": 12300},
        {"code": "NEGOCIOS", "discount": 25, "type": "percent", "uses": 67, "max_uses": 100, "revenue_impact": 34500, "discount_given": 8900},
        {"code": "WEEKEND50", "discount": 50, "type": "fixed", "uses": 34, "max_uses": 50, "revenue_impact": 18200, "discount_given": 1700},
        {"code": "PRIMEIRAESTADIA", "discount": 20, "type": "percent", "uses": 128, "max_uses": 300, "revenue_impact": 67800, "discount_given": 16950}
    ]
    return pd.DataFrame(promo_codes)

def calculate_kpis(df):
    """Calcula KPIs principais do negócio hoteleiro"""
    current_month = datetime.now().replace(day=1)
    last_month = (current_month - timedelta(days=1)).replace(day=1)
    
    # Dados do mês atual
    current_data = df[df['check_in'] >= current_month]
    last_month_data = df[(df['check_in'] >= last_month) & (df['check_in'] < current_month)]
    
    kpis = {}
    
    # Receita total
    kpis['revenue'] = current_data['total_price'].sum()
    kpis['revenue_last'] = last_month_data['total_price'].sum()
    kpis['revenue_change'] = ((kpis['revenue'] - kpis['revenue_last']) / kpis['revenue_last']) * 100 if kpis['revenue_last'] > 0 else 0
    
    # ADR (Average Daily Rate)
    kpis['adr'] = current_data['daily_rate'].mean()
    kpis['adr_last'] = last_month_data['daily_rate'].mean()
    kpis['adr_change'] = ((kpis['adr'] - kpis['adr_last']) / kpis['adr_last']) * 100 if kpis['adr_last'] > 0 else 0
    
    # Reservas
    kpis['bookings'] = len(current_data)
    kpis['bookings_last'] = len(last_month_data)
    kpis['bookings_change'] = ((kpis['bookings'] - kpis['bookings_last']) / kpis['bookings_last']) * 100 if kpis['bookings_last'] > 0 else 0
    
    # Taxa de ocupação estimada (simplificada)
    total_properties = 8  # número de propriedades
    days_in_month = datetime.now().day
    kpis['occupancy'] = (current_data['nights'].sum() / (total_properties * days_in_month)) * 100
    
    last_month_days = (current_month - timedelta(days=1)).day
    kpis['occupancy_last'] = (last_month_data['nights'].sum() / (total_properties * last_month_days)) * 100
    kpis['occupancy_change'] = kpis['occupancy'] - kpis['occupancy_last']
    
    return kpis

def create_revenue_chart(df):
    """Cria gráfico de evolução da receita"""
    # Agrupar por mês
    df['month'] = df['check_in'].dt.to_period('M')
    monthly_revenue = df.groupby('month').agg({
        'total_price': 'sum',
        'id': 'count'
    }).reset_index()
    
    monthly_revenue['month_str'] = monthly_revenue['month'].astype(str)
    
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Receita Mensal (R$)', 'Número de Reservas'),
        vertical_spacing=0.1,
        specs=[[{"secondary_y": False}], [{"secondary_y": False}]]
    )
    
    # Receita
    fig.add_trace(
        go.Scatter(
            x=monthly_revenue['month_str'], 
            y=monthly_revenue['total_price'],
            mode='lines+markers',
            name='Receita',
            line=dict(color='#2962ff', width=3),
            marker=dict(size=8)
        ),
        row=1, col=1
    )
    
    # Número de reservas
    fig.add_trace(
        go.Bar(
            x=monthly_revenue['month_str'], 
            y=monthly_revenue['id'],
            name='Reservas',
            marker_color='#1976d2'
        ),
        row=2, col=1
    )
    
    fig.update_layout(height=500, showlegend=False)
    fig.update_xaxes(title_text="Mês", row=2, col=1)
    fig.update_yaxes(title_text="Receita (R$)", row=1, col=1)
    fig.update_yaxes(title_text="Reservas", row=2, col=1)
    
    return fig

def create_property_performance_chart(df):
    """Cria gráfico de performance por propriedade"""
    property_stats = df.groupby('property_name').agg({
        'total_price': 'sum',
        'daily_rate': 'mean',
        'id': 'count'
    }).reset_index()
    
    property_stats = property_stats.sort_values('total_price', ascending=True)
    
    fig = go.Figure(go.Bar(
        x=property_stats['total_price'],
        y=property_stats['property_name'],
        orientation='h',
        marker=dict(
            color=property_stats['total_price'],
            colorscale='Viridis',
            showscale=True
        ),
        text=[f'R$ {x:,.0f}' for x in property_stats['total_price']],
        textposition='auto'
    ))
    
    fig.update_layout(
        title="Receita por Propriedade",
        xaxis_title="Receita Total (R$)",
        yaxis_title="Propriedade",
        height=400
    )
    
    return fig

def create_occupancy_calendar(df):
    """Cria calendário de ocupação"""
    # Simplificado - mostra distribuição de reservas por dia da semana
    df['weekday'] = df['check_in'].dt.day_name()
    df['week'] = df['check_in'].dt.isocalendar().week
    
    occupancy_data = df.groupby(['week', 'weekday']).size().reset_index(name='bookings')
    
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    occupancy_pivot = occupancy_data.pivot(index='week', columns='weekday', values='bookings').fillna(0)
    occupancy_pivot = occupancy_pivot.reindex(columns=weekdays)
    
    fig = go.Figure(data=go.Heatmap(
        z=occupancy_pivot.values,
        x=weekdays,
        y=occupancy_pivot.index,
        colorscale='RdYlBu_r',
        hoverongaps=False
    ))
    
    fig.update_layout(
        title="Mapa de Calor - Reservas por Semana",
        xaxis_title="Dia da Semana",
        yaxis_title="Semana do Ano",
        height=400
    )
    
    return fig

# Interface principal
def main():
    # Header principal
    st.markdown("""
    <div class="main-header">
        <h1>🏨 Stays Analytics Dashboard</h1>
        <p>Inteligência de negócios em tempo real para sua operação hoteleira</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Caregar dados
    with st.spinner('Carregando dados da API Stays...'):
        df_bookings, properties = generate_stays_demo_data()
        df_promos = generate_promo_codes_data()
    
    # Sidebar com filtros
    with st.sidebar:
        st.image("https://via.placeholder.com/150x50/2962ff/white?text=STAYS", width=150)
        
        st.markdown("### 🔍 Filtros")
        
        # Filtro de data
        date_range = st.date_input(
            "Período de Análise",
            value=[datetime.now() - timedelta(days=30), datetime.now()],
            max_value=datetime.now(),
            help="Selecione o período para análise"
        )
        
        # Filtro de região
        regions = st.multiselect(
            "Regiões",
            options=df_bookings['region'].unique(),
            default=df_bookings['region'].unique(),
            help="Selecione as regiões para análise"
        )
        
        # Filtro de tipo de propriedade
        property_types = st.multiselect(
            "Tipos de Propriedade",
            options=df_bookings['property_type'].unique(),
            default=df_bookings['property_type'].unique(),
            help="Selecione os tipos de propriedade"
        )
        
        # Filtro de status
        status_filter = st.multiselect(
            "Status das Reservas",
            options=df_bookings['status'].unique(),
            default=['confirmed'],
            help="Filtrar por status da reserva"
        )
    
    # Aplicar filtros
    filtered_df = df_bookings[
        (df_bookings['check_in'] >= pd.to_datetime(date_range[0])) &
        (df_bookings['check_in'] <= pd.to_datetime(date_range[1])) &
        (df_bookings['region'].isin(regions)) &
        (df_bookings['property_type'].isin(property_types)) &
        (df_bookings['status'].isin(status_filter))
    ]
    
    # Calcular KPIs
    kpis = calculate_kpis(df_bookings)
    
    # Métricas principais
    st.markdown("### 📊 KPIs Principais")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Receita Total",
            f"R$ {kpis['revenue']:,.2f}",
            f"{kpis['revenue_change']:+.1f}%",
            help="Receita total do período vs período anterior"
        )
    
    with col2:
        st.metric(
            "ADR Médio",
            f"R$ {kpis['adr']:.2f}",
            f"{kpis['adr_change']:+.1f}%",
            help="Average Daily Rate (Taxa Diária Média)"
        )
    
    with col3:
        st.metric(
            "Reservas",
            f"{kpis['bookings']:,}",
            f"{kpis['bookings_change']:+.1f}%",
            help="Número total de reservas"
        )
    
    with col4:
        st.metric(
            "Ocupação",
            f"{kpis['occupancy']:.1f}%",
            f"{kpis['occupancy_change']:+.1f}pp",
            help="Taxa de ocupação estimada"
        )
    
    st.markdown("---")
    
    # Gráficos principais
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📈 Evolução da Receita")
        revenue_chart = create_revenue_chart(filtered_df)
        st.plotly_chart(revenue_chart, use_container_width=True)
    
    with col2:
        st.markdown("### 🏢 Performance por Propriedade")
        property_chart = create_property_performance_chart(filtered_df)
        st.plotly_chart(property_chart, use_container_width=True)
    
    # Análise detalhada em tabs
    st.markdown("### 🔍 Análise Detalhada")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📅 Ocupação", "💰 Códigos Promocionais", "📋 Reservas", "🎯 Insights"])
    
    with tab1:
        st.markdown("#### Mapa de Calor - Ocupação")
        occupancy_chart = create_occupancy_calendar(filtered_df)
        st.plotly_chart(occupancy_chart, use_container_width=True)
        
        # Distribuição por região
        col1, col2 = st.columns(2)
        with col1:
            region_stats = filtered_df.groupby('region')['total_price'].sum().reset_index()
            fig_region = px.pie(region_stats, values='total_price', names='region', 
                               title="Receita por Região")
            st.plotly_chart(fig_region, use_container_width=True)
        
        with col2:
            type_stats = filtered_df.groupby('property_type')['total_price'].sum().reset_index()
            fig_type = px.pie(type_stats, values='total_price', names='property_type',
                             title="Receita por Tipo")
            st.plotly_chart(fig_type, use_container_width=True)
    
    with tab2:
        st.markdown("#### Performance dos Códigos Promocionais")
        
        # Métricas de promoções
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_revenue_promo = df_promos['revenue_impact'].sum()
            st.metric("Receita Adicional", f"R$ {total_revenue_promo:,.2f}")
        
        with col2:
            total_discount = df_promos['discount_given'].sum()
            st.metric("Desconto Total", f"R$ {total_discount:,.2f}")
        
        with col3:
            roi_promo = ((total_revenue_promo - total_discount) / total_discount) * 100
            st.metric("ROI Promoções", f"{roi_promo:.1f}%")
        
        # Tabela de códigos promocionais
        st.dataframe(
            df_promos.style.format({
                'revenue_impact': 'R$ {:,.2f}',
                'discount_given': 'R$ {:,.2f}',
                'discount': '{:.0f}%' if df_promos['type'].iloc[0] == 'percent' else 'R$ {:,.2f}'
            }),
            use_container_width=True
        )
        
        # Gráfico de performance dos códigos
        fig_promo = go.Figure()
        fig_promo.add_trace(go.Bar(
            x=df_promos['code'],
            y=df_promos['revenue_impact'],
            name='Receita Adicional',
            marker_color='#28a745'
        ))
        fig_promo.add_trace(go.Bar(
            x=df_promos['code'],
            y=-df_promos['discount_given'],  # Negativo para mostrar como custo
            name='Desconto Dado',
            marker_color='#dc3545'
        ))
        
        fig_promo.update_layout(
            title="Impacto dos Códigos Promocionais",
            xaxis_title="Código Promocional",
            yaxis_title="Valor (R$)",
            barmode='relative'
        )
        
        st.plotly_chart(fig_promo, use_container_width=True)
    
    with tab3:
        st.markdown("#### Reservas Recentes")
        
        # Filtros adicionais para reservas
        col1, col2 = st.columns(2)
        with col1:
            show_status = st.selectbox("Mostrar status", ['Todos', 'confirmed', 'pending', 'canceled'])
        with col2:
            show_recent = st.number_input("Mostrar últimas", min_value=5, max_value=100, value=20)
        
        # Filtrar e mostrar reservas
        reservas_display = filtered_df.copy()
        if show_status != 'Todos':
            reservas_display = reservas_display[reservas_display['status'] == show_status]
        
        reservas_display = reservas_display.sort_values('check_in', ascending=False).head(show_recent)
        
        # Formatação das colunas
        reservas_display['Propriedade'] = reservas_display['property_name']
        reservas_display['Hóspede'] = reservas_display['guest_name']
        reservas_display['Check-in'] = reservas_display['check_in'].dt.strftime('%d/%m/%Y')
        reservas_display['Check-out'] = reservas_display['check_out'].dt.strftime('%d/%m/%Y')
        reservas_display['Valor'] = reservas_display['total_price'].apply(lambda x: f"R$ {x:,.2f}")
        reservas_display['Status'] = reservas_display['status']
        
        st.dataframe(
            reservas_display[['Propriedade', 'Hóspede', 'Check-in', 'Check-out', 'Valor', 'Status']],
            use_container_width=True,
            hide_index=True
        )
    
    with tab4:
        st.markdown("#### 🎯 Insights e Recomendações")
        
        # Análise automática dos dados
        total_revenue = filtered_df['total_price'].sum()
        best_property = filtered_df.groupby('property_name')['total_price'].sum().idxmax()
        best_region = filtered_df.groupby('region')['total_price'].sum().idxmax()
        avg_stay = filtered_df['nights'].mean()
        
        # Cards de insights
        insights = [
            {
                "tipo": "success",
                "titulo": "🏆 Propriedade Top",
                "conteudo": f"{best_property} é a propriedade com melhor performance, representando {(filtered_df[filtered_df['property_name'] == best_property]['total_price'].sum() / total_revenue * 100):.1f}% da receita total."
            },
            {
                "tipo": "warning",
                "titulo": "📍 Foco Regional",
                "conteudo": f"{best_region} é a região mais lucrativa. Considere expandir o portfólio nesta região."
            },
            {
                "tipo": "info",
                "titulo": "📊 Duração Média",
                "conteudo": f"Estadias têm duração média de {avg_stay:.1f} noites. Promoções para estadias mais longas podem aumentar o RevPAR."
            }
        ]
        
        for insight in insights:
            st.markdown(f"""
            <div class="alert-card alert-{insight['tipo']}">
                <h5>{insight['titulo']}</h5>
                <p>{insight['conteudo']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Recomendações estratégicas
        st.markdown("##### 🚀 Recomendações Estratégicas")
        
        recommendations = [
            "Implementar dynamic pricing para fins de semana (potencial aumento de 20% na receita)",
            f"Expandir portfólio em {best_region} baseado na alta demanda",
            "Criar pacotes para estadias longas (7+ noites) com desconto progressivo",
            "Otimizar códigos promocionais com base no ROI demonstrado",
            "Implementar programa de fidelidade para hóspedes recorrentes"
        ]
        
        for i, rec in enumerate(recommendations, 1):
            st.success(f"**{i}.** {rec}")

    # Footer
    st.markdown("---")
    st.markdown("### 📞 Próximos Passos")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Gerar Relatório Completo", type="primary"):
            st.balloons()
            st.success("Relatório enviado para seu email!")
    
    with col2:
        if st.button("🔄 Atualizar Dados"):
            st.cache_data.clear()
            st.success("Cache limpo! Dados atualizados.")
            st.rerun()
    
    with col3:
        if st.button("💬 Agendar Reunião"):
            st.info("Redirecionando para calendário de reuniões...")

if __name__ == "__main__":
    main()
