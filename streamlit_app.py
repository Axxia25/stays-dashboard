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
import json

# Configuração da página
st.set_page_config(
    page_title="EduAnalytics | Dashboard Escolar Inteligente",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado elegante (mantendo o design)
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
        background: linear-gradient(135deg, #2c5aa0 0%, #16537e 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 3rem;
        box-shadow: 0 20px 40px rgba(44, 90, 160, 0.15);
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
        background: linear-gradient(90deg, #2c5aa0, #16537e);
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
        background: linear-gradient(135deg, #2c5aa0 0%, #16537e 100%);
        color: white;
        box-shadow: 0 8px 16px rgba(44, 90, 160, 0.3);
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
        background: linear-gradient(135deg, #2c5aa0 0%, #16537e 100%);
        border-radius: 3px;
    }
    
    /* Cards de turma/aluno elegantes */
    .student-card-premium {
        background: white;
        border-radius: 16px;
        padding: 1.8rem;
        margin-bottom: 1.2rem;
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .student-card-premium:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
    }
    
    .student-card-premium.high-performance::before {
        content: '';
        position: absolute;
        left: 0;
        top: 0;
        width: 6px;
        height: 100%;
        background: linear-gradient(180deg, #10b981 0%, #059669 100%);
    }
    
    .student-card-premium.medium-performance::before {
        content: '';
        position: absolute;
        left: 0;
        top: 0;
        width: 6px;
        height: 100%;
        background: linear-gradient(180deg, #f59e0b 0%, #d97706 100%);
    }
    
    .student-card-premium.low-performance::before {
        content: '';
        position: absolute;
        left: 0;
        top: 0;
        width: 6px;
        height: 100%;
        background: linear-gradient(180deg, #ef4444 0%, #dc2626 100%);
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
    
    /* Filter container */
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
</style>
""", unsafe_allow_html=True)

# Funções de dados escolares
@st.cache_data(ttl=300)
def generate_school_comprehensive_data():
    """Gera dataset completo para escola com 1000 alunos"""
    fake = Faker('pt_BR')
    np.random.seed(42)
    
    # Estrutura da escola
    series_structure = {
        "Educação Infantil": {
            "levels": ["Maternal I", "Maternal II", "Pré I", "Pré II"],
            "students_per_class": 20,
            "classes_per_level": 2,
            "monthly_fee": 800
        },
        "Ensino Fundamental I": {
            "levels": ["1º Ano", "2º Ano", "3º Ano", "4º Ano", "5º Ano"],
            "students_per_class": 25,
            "classes_per_level": 2,
            "monthly_fee": 950
        },
        "Ensino Fundamental II": {
            "levels": ["6º Ano", "7º Ano", "8º Ano", "9º Ano"],
            "students_per_class": 30,
            "classes_per_level": 2,
            "monthly_fee": 1100
        },
        "Ensino Médio": {
            "levels": ["1ª Série", "2ª Série", "3ª Série"],
            "students_per_class": 35,
            "classes_per_level": 2,
            "monthly_fee": 1300
        }
    }
    
    # Gerar dados de alunos
    students = []
    student_id = 1
    
    for segment, data in series_structure.items():
        for level in data["levels"]:
            for class_num in range(1, data["classes_per_level"] + 1):
                for student_num in range(data["students_per_class"]):
                    birth_year = {
                        "Educação Infantil": np.random.randint(2018, 2021),
                        "Ensino Fundamental I": np.random.randint(2013, 2018),
                        "Ensino Fundamental II": np.random.randint(2009, 2013),
                        "Ensino Médio": np.random.randint(2006, 2009)
                    }[segment]
                    
                    student = {
                        "student_id": f"EST{student_id:04d}",
                        "name": fake.name(),
                        "segment": segment,
                        "level": level,
                        "class": f"{level} - Turma {class_num}",
                        "birth_date": fake.date_of_birth(minimum_age=datetime.now().year - birth_year - 1, maximum_age=datetime.now().year - birth_year + 1),
                        "gender": np.random.choice(["Masculino", "Feminino"], p=[0.51, 0.49]),
                        "monthly_fee": data["monthly_fee"],
                        "scholarship": np.random.choice([0, 10, 25, 50, 100], p=[0.7, 0.15, 0.1, 0.04, 0.01]),
                        "parent_name": fake.name(),
                        "parent_email": fake.email(),
                        "parent_phone": fake.phone_number(),
                        "address": fake.address(),
                        "enrollment_date": fake.date_between(start_date='-2y', end_date='today'),
                        "status": np.random.choice(["Ativo", "Inativo", "Transferido"], p=[0.92, 0.05, 0.03])
                    }
                    students.append(student)
                    student_id += 1
    
    students_df = pd.DataFrame(students)
    
    # Gerar dados acadêmicos (notas por bimestre)
    academic_data = []
    subjects = {
        "Educação Infantil": ["Linguagem", "Matemática", "Natureza", "Artes", "Movimento"],
        "Ensino Fundamental I": ["Português", "Matemática", "Ciências", "História", "Geografia", "Artes", "Ed. Física"],
        "Ensino Fundamental II": ["Português", "Matemática", "Ciências", "História", "Geografia", "Inglês", "Artes", "Ed. Física"],
        "Ensino Médio": ["Português", "Matemática", "Física", "Química", "Biologia", "História", "Geografia", "Inglês", "Filosofia", "Sociologia"]
    }
    
    for _, student in students_df.iterrows():
        if student['status'] == 'Ativo':
            student_subjects = subjects[student['segment']]
            
            # Definir perfil do aluno (influencia nas notas)
            performance_profile = np.random.choice(["Alto", "Médio", "Baixo"], p=[0.25, 0.65, 0.1])
            base_performance = {"Alto": 8.5, "Médio": 7.0, "Baixo": 5.5}[performance_profile]
            
            for subject in student_subjects:
                for bimester in [1, 2, 3, 4]:
                    # Variação natural das notas
                    note = np.random.normal(base_performance, 1.2)
                    note = max(0, min(10, note))  # Limitar entre 0 e 10
                    
                    # Absences
                    max_classes = 20  # 20 aulas por bimestre por matéria
                    absences = np.random.poisson(2 if performance_profile == "Alto" else 4 if performance_profile == "Médio" else 7)
                    absences = min(absences, max_classes)
                    
                    academic_record = {
                        "student_id": student['student_id'],
                        "segment": student['segment'],
                        "level": student['level'],
                        "class": student['class'],
                        "subject": subject,
                        "bimester": bimester,
                        "grade": round(note, 1),
                        "absences": absences,
                        "max_classes": max_classes,
                        "performance_profile": performance_profile,
                        "year": 2025
                    }
                    academic_data.append(academic_record)
    
    academic_df = pd.DataFrame(academic_data)
    
    # Gerar dados financeiros
    financial_data = []
    for _, student in students_df.iterrows():
        if student['status'] == 'Ativo':
            # Status de pagamento baseado no perfil socioeconômico
            payment_profile = np.random.choice(["Pontual", "Atraso Eventual", "Problemático"], p=[0.75, 0.20, 0.05])
            
            for month in range(1, 13):  # 12 meses
                monthly_value = student['monthly_fee'] * (1 - student['scholarship']/100)
                
                if payment_profile == "Pontual":
                    payment_status = np.random.choice(["Pago", "Pago"], p=[0.95, 0.05])
                    days_late = 0 if payment_status == "Pago" else np.random.randint(1, 5)
                elif payment_profile == "Atraso Eventual":
                    payment_status = np.random.choice(["Pago", "Em Atraso"], p=[0.8, 0.2])
                    days_late = 0 if payment_status == "Pago" else np.random.randint(1, 30)
                else:  # Problemático
                    payment_status = np.random.choice(["Pago", "Em Atraso", "Inadimplente"], p=[0.6, 0.25, 0.15])
                    days_late = 0 if payment_status == "Pago" else np.random.randint(15, 90)
                
                financial_record = {
                    "student_id": student['student_id'],
                    "student_name": student['name'],
                    "segment": student['segment'],
                    "level": student['level'],
                    "month": month,
                    "year": 2025,
                    "monthly_fee": monthly_value,
                    "payment_status": payment_status,
                    "days_late": days_late,
                    "payment_profile": payment_profile
                }
                financial_data.append(financial_record)
    
    financial_df = pd.DataFrame(financial_data)
    
    # Gerar dados de funcionários
    employees = []
    departments = {
        "Pedagógico": {"count": 45, "avg_salary": 4500, "positions": ["Professor", "Coordenador", "Orientador"]},
        "Administrativo": {"count": 15, "avg_salary": 3200, "positions": ["Secretário", "Auxiliar", "Analista"]},
        "Operacional": {"count": 12, "avg_salary": 2100, "positions": ["Auxiliar Limpeza", "Porteiro", "Manutenção"]},
        "Direção": {"count": 5, "avg_salary": 8500, "positions": ["Diretor", "Vice-Diretor", "Supervisor"]}
    }
    
    employee_id = 1
    for dept, data in departments.items():
        for _ in range(data["count"]):
            employee = {
                "employee_id": f"FUNC{employee_id:03d}",
                "name": fake.name(),
                "department": dept,
                "position": np.random.choice(data["positions"]),
                "salary": np.random.normal(data["avg_salary"], data["avg_salary"] * 0.2),
                "hire_date": fake.date_between(start_date='-5y', end_date='today'),
                "status": np.random.choice(["Ativo", "Afastado", "Férias"], p=[0.92, 0.05, 0.03]),
                "absences_month": np.random.poisson(2)
            }
            employees.append(employee)
            employee_id += 1
    
    employees_df = pd.DataFrame(employees)
    
    return students_df, academic_df, financial_df, employees_df, series_structure

def calculate_school_kpis(students_df, academic_df, financial_df, employees_df):
    """Calcula KPIs principais da escola"""
    kpis = {}
    
    # KPIs Acadêmicos
    current_grades = academic_df[academic_df['bimester'] == academic_df['bimester'].max()]
    kpis['avg_grade'] = current_grades['grade'].mean()
    kpis['approval_rate'] = (current_grades['grade'] >= 6.0).mean() * 100
    kpis['students_at_risk'] = len(current_grades[current_grades['grade'] < 5.0]['student_id'].unique())
    
    # KPIs Financeiros
    current_month = datetime.now().month
    current_financial = financial_df[financial_df['month'] == current_month]
    
    total_revenue_potential = current_financial['monthly_fee'].sum()
    paid_revenue = current_financial[current_financial['payment_status'] == 'Pago']['monthly_fee'].sum()
    kpis['collection_rate'] = (paid_revenue / total_revenue_potential) * 100 if total_revenue_potential > 0 else 0
    kpis['monthly_revenue'] = paid_revenue
    kpis['defaulting_students'] = len(current_financial[current_financial['payment_status'] == 'Inadimplente'])
    
    # KPIs Operacionais
    active_students = len(students_df[students_df['status'] == 'Ativo'])
    kpis['total_students'] = active_students
    kpis['student_teacher_ratio'] = active_students / len(employees_df[employees_df['department'] == 'Pedagógico'])
    
    # KPIs de Pessoas
    kpis['employee_absences'] = employees_df['absences_month'].mean()
    kpis['teacher_count'] = len(employees_df[employees_df['department'] == 'Pedagógico'])
    
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

def create_grade_evolution_chart(academic_df):
    """Gráfico de evolução das notas por bimestre"""
    bimester_grades = academic_df.groupby('bimester')['grade'].mean().reset_index()
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=bimester_grades['bimester'],
        y=bimester_grades['grade'],
        mode='lines+markers',
        name='Média Geral',
        line=dict(color='rgba(44, 90, 160, 1)', width=4, shape='spline'),
        marker=dict(size=12, color='rgba(44, 90, 160, 1)', line=dict(color='white', width=3)),
        fill='tonexty',
        fillcolor='rgba(44, 90, 160, 0.1)',
        hovertemplate='<b>%{x}º Bimestre</b><br>Média: %{y:.1f}<extra></extra>'
    ))
    
    # Linha de meta (6.0)
    fig.add_hline(y=6.0, line_dash="dash", line_color="red", 
                  annotation_text="Meta de Aprovação (6.0)")
    
    fig.update_layout(
        title={'text': '<b>Evolução das Notas por Bimestre</b>', 'font': {'size': 24, 'family': 'Inter'}, 'x': 0.02},
        xaxis_title="Bimestre", yaxis_title="Nota Média", height=400,
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter", size=14), hovermode='x unified', showlegend=False
    )
    
    fig.update_xaxes(gridcolor='rgba(0,0,0,0.05)', showgrid=True, zeroline=False)
    fig.update_yaxes(gridcolor='rgba(0,0,0,0.05)', showgrid=True, zeroline=False, range=[0, 10])
    
    return fig

def create_financial_overview_chart(financial_df):
    """Gráfico overview financeiro"""
    monthly_summary = financial_df.groupby(['month', 'payment_status'])['monthly_fee'].sum().reset_index()
    monthly_pivot = monthly_summary.pivot(index='month', columns='payment_status', values='monthly_fee').fillna(0)
    
    fig = go.Figure()
    
    if 'Pago' in monthly_pivot.columns:
        fig.add_trace(go.Bar(
            x=monthly_pivot.index,
            y=monthly_pivot['Pago'],
            name='Receita Recebida',
            marker_color='rgba(16, 185, 129, 0.8)'
        ))
    
    if 'Em Atraso' in monthly_pivot.columns:
        fig.add_trace(go.Bar(
            x=monthly_pivot.index,
            y=monthly_pivot['Em Atraso'],
            name='Em Atraso',
            marker_color='rgba(245, 158, 11, 0.8)'
        ))
    
    if 'Inadimplente' in monthly_pivot.columns:
        fig.add_trace(go.Bar(
            x=monthly_pivot.index,
            y=monthly_pivot['Inadimplente'],
            name='Inadimplente',
            marker_color='rgba(239, 68, 68, 0.8)'
        ))
    
    fig.update_layout(
        title={'text': '<b>Receita Mensal por Status</b>', 'font': {'size': 20, 'family': 'Inter'}, 'x': 0.02},
        xaxis_title="Mês", yaxis_title="Receita (R$)", height=400,
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter", size=12), barmode='stack'
    )
    
    return fig

def create_performance_by_segment_chart(academic_df):
    """Gráfico de performance por segmento"""
    segment_performance = academic_df.groupby('segment')['grade'].mean().sort_values(ascending=True)
    
    fig = go.Figure(go.Bar(
        y=segment_performance.index,
        x=segment_performance.values,
        orientation='h',
        marker=dict(
            color=segment_performance.values,
            colorscale=[[0, '#ef4444'], [0.6, '#f59e0b'], [1, '#10b981']],
            line=dict(color='rgba(255,255,255,0.2)', width=1)
        ),
        text=[f'{x:.1f}' for x in segment_performance.values],
        textposition='auto',
        hovertemplate='<b>%{y}</b><br>Média: %{x:.1f}<extra></extra>'
    ))
    
    # Linha de meta
    fig.add_vline(x=6.0, line_dash="dash", line_color="red", 
                  annotation_text="Meta (6.0)")
    
    fig.update_layout(
        title={'text': '<b>Performance Acadêmica por Segmento</b>', 'font': {'size': 20, 'family': 'Inter'}, 'x': 0.02},
        xaxis_title="Nota Média", height=400,
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter", size=12)
    )
    
    fig.update_xaxes(gridcolor='rgba(0,0,0,0.05)', showgrid=True, zeroline=False, range=[0, 10])
    fig.update_yaxes(gridcolor='rgba(0,0,0,0.05)', showgrid=False)
    
    return fig

# Interface principal
def main():
    # Header elegante
    st.markdown("""
    <div class="elegant-header">
        <h1>EduAnalytics</h1>
        <p>Dashboard Inteligente de Gestão Escolar</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Carregamento de dados
    with st.spinner('🚀 Carregando dados da escola...'):
        students_df, academic_df, financial_df, employees_df, series_structure = generate_school_comprehensive_data()
        time.sleep(0.5)
    
    # Sidebar com filtros globais
    with st.sidebar:
        st.markdown('<div class="filter-container">', unsafe_allow_html=True)
        st.markdown('<div class="filter-title">🎯 Filtros Globais</div>', unsafe_allow_html=True)
        
        # Filtro de segmento
        segments = st.multiselect(
            "📚 Segmentos de Ensino",
            options=students_df['segment'].unique(),
            default=students_df['segment'].unique()
        )
        
        # Filtro de nível
        available_levels = students_df[students_df['segment'].isin(segments)]['level'].unique()
        levels = st.multiselect(
            "📖 Níveis de Ensino",
            options=available_levels,
            default=available_levels
        )
        
        # Filtro de bimestre
        bimester = st.selectbox(
            "📅 Bimestre",
            options=[1, 2, 3, 4],
            index=3  # 4º bimestre como padrão
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Seleção de dashboard
        st.markdown('<div class="filter-container">', unsafe_allow_html=True)
        st.markdown('<div class="filter-title">📊 Dashboard Ativo</div>', unsafe_allow_html=True)
        
        dashboard_selection = st.selectbox(
            "Selecione o Dashboard:",
            [
                "📊 Visão Executiva",
                "🎓 Dashboard Acadêmico", 
                "💰 Analytics Financeiro",
                "👥 Gestão de Pessoas",
                "🏫 Dashboard Operacional",
                "🔍 Business Intelligence"
            ]
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Filtrar dados
    filtered_students = students_df[
        (students_df['segment'].isin(segments)) &
        (students_df['level'].isin(levels))
    ]
    
    filtered_academic = academic_df[
        (academic_df['segment'].isin(segments)) &
        (academic_df['level'].isin(levels)) &
        (academic_df['bimester'] == bimester)
    ]
    
    filtered_financial = financial_df[
        (financial_df['segment'].isin(segments)) &
        (financial_df['level'].isin(levels))
    ]
    
    # Calcular KPIs
    kpis = calculate_school_kpis(filtered_students, filtered_academic, filtered_financial, employees_df)
    
    # Renderizar dashboard selecionado
    if dashboard_selection == "📊 Visão Executiva":
        render_executive_dashboard(filtered_students, filtered_academic, filtered_financial, employees_df, kpis)
    elif dashboard_selection == "🎓 Dashboard Acadêmico":
        render_academic_dashboard(filtered_students, filtered_academic, kpis)
    elif dashboard_selection == "💰 Analytics Financeiro":
        render_financial_dashboard(filtered_students, filtered_financial, kpis)
    elif dashboard_selection == "👥 Gestão de Pessoas":
        render_people_dashboard(employees_df, students_df)
    elif dashboard_selection == "🏫 Dashboard Operacional":
        render_operational_dashboard(filtered_students, series_structure)
    elif dashboard_selection == "🔍 Business Intelligence":
        render_business_intelligence(filtered_students, filtered_academic, filtered_financial, kpis)

def render_executive_dashboard(students_df, academic_df, financial_df, employees_df, kpis):
    """Dashboard Executivo - Visão Geral da Diretoria"""
    st.markdown("## 📊 Dashboard Executivo")
    
    # KPIs principais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(create_elegant_metric_card("Total de Alunos", str(kpis['total_students']), 3.2, "👥"), unsafe_allow_html=True)
    
    with col2:
        st.markdown(create_elegant_metric_card("Média Geral", f"{kpis['avg_grade']:.1f}", 5.1, "📊"), unsafe_allow_html=True)
    
    with col3:
        st.markdown(create_elegant_metric_card("Taxa de Cobrança", f"{kpis['collection_rate']:.1f}%", -2.3, "💰"), unsafe_allow_html=True)
    
    with col4:
        st.markdown(create_elegant_metric_card("Receita Mensal", f"R$ {kpis['monthly_revenue']:,.0f}", 1.8, "💎"), unsafe_allow_html=True)
    
    # Gráficos principais
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="elegant-section">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Performance Acadêmica</div>', unsafe_allow_html=True)
        grade_evolution = create_grade_evolution_chart(academic_df)
        st.plotly_chart(grade_evolution, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="elegant-section">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Receita por Status</div>', unsafe_allow_html=True)
        financial_chart = create_financial_overview_chart(financial_df)
        st.plotly_chart(financial_chart, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Alertas executivos
    st.markdown('<div class="elegant-section">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Alertas Executivos</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if kpis['avg_grade'] >= 7.0:
            st.markdown(f"""
            <div class="alert-premium success">
                <div class="alert-title">🎉 Excelência Acadêmica</div>
                <p>Média geral de {kpis['avg_grade']:.1f} - acima da meta!</p>
            </div>
            """, unsafe_allow_html=True)
        elif kpis['avg_grade'] < 6.0:
            st.markdown(f"""
            <div class="alert-premium danger">
                <div class="alert-title">⚠️ Atenção Acadêmica</div>
                <p>Média geral de {kpis['avg_grade']:.1f} - abaixo da meta</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        if kpis['students_at_risk'] > 0:
            st.markdown(f"""
            <div class="alert-premium warning">
                <div class="alert-title">📚 Alunos em Risco</div>
                <p>{kpis['students_at_risk']} estudantes com média < 5.0</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col3:
        if kpis['collection_rate'] < 90:
            st.markdown(f"""
            <div class="alert-premium warning">
                <div class="alert-title">💰 Taxa de Cobrança</div>
                <p>Taxa em {kpis['collection_rate']:.1f}% - ação necessária</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="alert-premium success">
                <div class="alert-title">💰 Cobrança Eficiente</div>
                <p>Taxa de {kpis['collection_rate']:.1f}% - excelente!</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_academic_dashboard(students_df, academic_df, kpis):
    """Dashboard Acadêmico Detalhado"""
    st.markdown("## 🎓 Dashboard Acadêmico")
    
    # Métricas acadêmicas
    col1, col2, col3, col4, col5 = st.columns(5)
    
    # Calcular métricas com validação
    if not academic_df.empty:
        approval_rate = (academic_df['grade'] >= 6.0).mean() * 100
        excellence_rate = (academic_df['grade'] >= 9.0).mean() * 100
        avg_absences = academic_df['absences'].mean()
    else:
        approval_rate = 0.0
        excellence_rate = 0.0
        avg_absences = 0.0
    
    # Tratar valores NaN
    avg_grade_display = kpis.get('avg_grade', 0.0)
    if pd.isna(avg_grade_display):
        avg_grade_display = 0.0
        
    students_at_risk = kpis.get('students_at_risk', 0)
    
    with col1:
        st.markdown(create_elegant_metric_card("Média Geral", f"{avg_grade_display:.1f}", 5.1, "📊"), unsafe_allow_html=True)
    
    with col2:
        st.markdown(create_elegant_metric_card("Taxa Aprovação", f"{approval_rate:.1f}%", 3.2, "✅"), unsafe_allow_html=True)
    
    with col3:
        st.markdown(create_elegant_metric_card("Taxa Excelência", f"{excellence_rate:.1f}%", 8.5, "🌟"), unsafe_allow_html=True)
    
    with col4:
        st.markdown(create_elegant_metric_card("Alunos em Risco", str(students_at_risk), -15.2, "⚠️"), unsafe_allow_html=True)
    
    with col5:
        st.markdown(create_elegant_metric_card("Faltas Médias", f"{avg_absences:.1f}", -5.3, "📅"), unsafe_allow_html=True)
    
    # Performance por segmento
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 Performance por Segmento")
        performance_chart = create_performance_by_segment_chart(academic_df)
        st.plotly_chart(performance_chart, use_container_width=True)
    
    with col2:
        st.markdown("### 📚 Distribuição de Notas")
        fig_histogram = px.histogram(
            academic_df, 
            x='grade', 
            bins=20,
            title="Distribuição das Notas",
            color_discrete_sequence=['#2c5aa0']
        )
        fig_histogram.add_vline(x=6.0, line_dash="dash", line_color="red", annotation_text="Meta")
        fig_histogram.update_layout(font=dict(family="Inter"))
        st.plotly_chart(fig_histogram, use_container_width=True)
    
    # Top/Bottom performers
    st.markdown("### 🏆 Performance por Turma")
    
    class_performance = academic_df.groupby('class').agg({
        'grade': 'mean',
        'student_id': 'count'
    }).reset_index().sort_values('grade', ascending=False)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🥇 Melhores Turmas")
        top_classes = class_performance.head(5)
        for _, row in top_classes.iterrows():
            performance_level = "high-performance" if row['grade'] >= 7.5 else "medium-performance"
            st.markdown(f"""
            <div class="student-card-premium {performance_level}">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong>{row['class']}</strong><br>
                        <small>{row['student_id']} alunos</small>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-size: 1.4rem; font-weight: bold; color: #2c5aa0;">
                            {row['grade']:.1f}
                        </div>
                        <div style="font-size: 0.9rem; color: #666;">Média</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### 📉 Turmas Que Precisam de Atenção")
        bottom_classes = class_performance.tail(5)
        for _, row in bottom_classes.iterrows():
            performance_level = "low-performance" if row['grade'] < 6.0 else "medium-performance"
            st.markdown(f"""
            <div class="student-card-premium {performance_level}">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong>{row['class']}</strong><br>
                        <small>{row['student_id']} alunos</small>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-size: 1.4rem; font-weight: bold; color: #ef4444;">
                            {row['grade']:.1f}
                        </div>
                        <div style="font-size: 0.9rem; color: #666;">Média</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

def render_financial_dashboard(students_df, financial_df, kpis):
    """Dashboard Financeiro Detalhado"""
    st.markdown("## 💰 Analytics Financeiro")
    
    # Métricas financeiras
    current_month = datetime.now().month
    current_financial = financial_df[financial_df['month'] == current_month]
    
    total_potential = current_financial['monthly_fee'].sum()
    total_received = current_financial[current_financial['payment_status'] == 'Pago']['monthly_fee'].sum()
    total_overdue = current_financial[current_financial['payment_status'] == 'Em Atraso']['monthly_fee'].sum()
    total_defaulting = current_financial[current_financial['payment_status'] == 'Inadimplente']['monthly_fee'].sum()
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(create_elegant_metric_card("Receita Potencial", f"R$ {total_potential:,.0f}", 2.1, "🎯"), unsafe_allow_html=True)
    
    with col2:
        st.markdown(create_elegant_metric_card("Receita Recebida", f"R$ {total_received:,.0f}", 1.8, "💰"), unsafe_allow_html=True)
    
    with col3:
        st.markdown(create_elegant_metric_card("Em Atraso", f"R$ {total_overdue:,.0f}", 15.2, "⏰"), unsafe_allow_html=True)
    
    with col4:
        st.markdown(create_elegant_metric_card("Inadimplência", f"R$ {total_defaulting:,.0f}", -8.1, "❌"), unsafe_allow_html=True)
    
    with col5:
        st.markdown(create_elegant_metric_card("Taxa Cobrança", f"{kpis['collection_rate']:.1f}%", -2.3, "📊"), unsafe_allow_html=True)
    
    # Análise de inadimplência
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Evolução Mensal da Receita")
        financial_overview = create_financial_overview_chart(financial_df)
        st.plotly_chart(financial_overview, use_container_width=True)
    
    with col2:
        st.markdown("### 🎯 Inadimplência por Segmento")
        segment_default = financial_df[financial_df['payment_status'] == 'Inadimplente'].groupby('segment')['monthly_fee'].sum()
        
        if not segment_default.empty:
            fig_default = px.pie(
                values=segment_default.values,
                names=segment_default.index,
                title="Inadimplência por Segmento",
                color_discrete_sequence=['#ef4444', '#f59e0b', '#10b981', '#3b82f6']
            )
            fig_default.update_layout(font=dict(family="Inter"))
            st.plotly_chart(fig_default, use_container_width=True)
        else:
            st.info("😊 Nenhuma inadimplência registrada!")
    
    # Relatório de inadimplentes
    st.markdown("### 📋 Relatório de Inadimplência")
    
    defaulters = current_financial[current_financial['payment_status'] == 'Inadimplente'].merge(
        students_df[['student_id', 'name', 'parent_name', 'parent_phone']], 
        on='student_id'
    )
    
    if not defaulters.empty:
        # Exibir tabela de inadimplentes
        st.dataframe(
            defaulters[['name', 'segment', 'level', 'monthly_fee', 'parent_name', 'parent_phone']].rename(columns={
                'name': 'Aluno',
                'segment': 'Segmento',
                'level': 'Nível',
                'monthly_fee': 'Valor (R$)',
                'parent_name': 'Responsável',
                'parent_phone': 'Telefone'
            }),
            use_container_width=True,
            hide_index=True
        )
        
        # Botão para exportar
        if st.button("📊 Exportar Relatório de Inadimplência"):
            # Simular exportação
            st.success("✅ Relatório exportado com sucesso!")
            st.balloons()
    else:
        st.success("🎉 Parabéns! Não há inadimplentes no momento.")

def render_people_dashboard(employees_df, students_df):
    """Dashboard de Gestão de Pessoas"""
    st.markdown("## 👥 Gestão de Pessoas")
    
    # Métricas de RH
    active_employees = len(employees_df[employees_df['status'] == 'Ativo'])
    avg_absences = employees_df['absences_month'].mean()
    total_payroll = employees_df[employees_df['status'] == 'Ativo']['salary'].sum()
    student_teacher_ratio = len(students_df) / len(employees_df[employees_df['department'] == 'Pedagógico'])
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(create_elegant_metric_card("Funcionários Ativos", str(active_employees), 2.1, "👥"), unsafe_allow_html=True)
    
    with col2:
        st.markdown(create_elegant_metric_card("Faltas Médias/Mês", f"{avg_absences:.1f}", -8.2, "📅"), unsafe_allow_html=True)
    
    with col3:
        st.markdown(create_elegant_metric_card("Folha Salarial", f"R$ {total_payroll:,.0f}", 3.5, "💰"), unsafe_allow_html=True)
    
    with col4:
        st.markdown(create_elegant_metric_card("Alunos/Professor", f"{student_teacher_ratio:.1f}", 1.2, "📚"), unsafe_allow_html=True)
    
    # Análise por departamento
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 👥 Funcionários por Departamento")
        dept_count = employees_df['department'].value_counts()
        
        fig_dept = px.bar(
            x=dept_count.index,
            y=dept_count.values,
            title="Distribuição por Departamento",
            color=dept_count.values,
            color_continuous_scale=[[0, '#2c5aa0'], [1, '#16537e']]
        )
        fig_dept.update_layout(font=dict(family="Inter"), showlegend=False)
        st.plotly_chart(fig_dept, use_container_width=True)
    
    with col2:
        st.markdown("### 💰 Média Salarial por Departamento")
        salary_by_dept = employees_df.groupby('department')['salary'].mean().sort_values(ascending=False)
        
        fig_salary = px.bar(
            y=salary_by_dept.index,
            x=salary_by_dept.values,
            orientation='h',
            title="Média Salarial por Departamento",
            color=salary_by_dept.values,
            color_continuous_scale=[[0, '#2c5aa0'], [1, '#16537e']]
        )
        fig_salary.update_layout(font=dict(family="Inter"), showlegend=False)
        st.plotly_chart(fig_salary, use_container_width=True)
    
    # Análise de absenteísmo
    st.markdown("### 📊 Análise de Absenteísmo")
    
    dept_absences = employees_df.groupby('department')['absences_month'].mean().sort_values(ascending=False)
    
    for dept in dept_absences.index:
        avg_abs = dept_absences[dept]
        color = "#ef4444" if avg_abs > 3 else "#f59e0b" if avg_abs > 2 else "#10b981"
        
        st.markdown(f"""
        <div style="background: white; border-radius: 12px; padding: 1rem; margin: 0.5rem 0; border-left: 4px solid {color};">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <strong>{dept}</strong><br>
                    <small>{len(employees_df[employees_df['department'] == dept])} funcionários</small>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 1.2rem; font-weight: bold; color: {color};">
                        {avg_abs:.1f} faltas/mês
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def render_operational_dashboard(students_df, series_structure):
    """Dashboard Operacional"""
    st.markdown("## 🏫 Dashboard Operacional")
    
    # Análise de ocupação
    total_capacity = sum([
        data['students_per_class'] * data['classes_per_level'] * len(data['levels'])
        for data in series_structure.values()
    ])
    
    current_students = len(students_df[students_df['status'] == 'Ativo'])
    occupancy_rate = (current_students / total_capacity) * 100
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(create_elegant_metric_card("Capacidade Total", str(total_capacity), 0, "🏫"), unsafe_allow_html=True)
    
    with col2:
        st.markdown(create_elegant_metric_card("Alunos Ativos", str(current_students), 3.2, "👥"), unsafe_allow_html=True)
    
    with col3:
        st.markdown(create_elegant_metric_card("Taxa Ocupação", f"{occupancy_rate:.1f}%", 2.8, "📊"), unsafe_allow_html=True)
    
    with col4:
        available_spots = total_capacity - current_students
        st.markdown(create_elegant_metric_card("Vagas Disponíveis", str(available_spots), -5.2, "🎯"), unsafe_allow_html=True)
    
    # Ocupação por segmento
    st.markdown("### 📊 Ocupação por Segmento")
    
    for segment, data in series_structure.items():
        segment_capacity = data['students_per_class'] * data['classes_per_level'] * len(data['levels'])
        segment_students = len(students_df[(students_df['segment'] == segment) & (students_df['status'] == 'Ativo')])
        segment_occupancy = (segment_students / segment_capacity) * 100
        
        color = "#10b981" if segment_occupancy >= 90 else "#f59e0b" if segment_occupancy >= 70 else "#ef4444"
        
        st.markdown(f"""
        <div style="background: white; border-radius: 12px; padding: 1.5rem; margin: 1rem 0; border-left: 4px solid {color};">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <strong>{segment}</strong><br>
                    <small>{segment_students}/{segment_capacity} alunos</small>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 1.4rem; font-weight: bold; color: {color};">
                        {segment_occupancy:.1f}%
                    </div>
                    <div style="font-size: 0.9rem; color: #666;">Ocupação</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def render_business_intelligence(students_df, academic_df, financial_df, kpis):
    """Business Intelligence e Simulações"""
    st.markdown("## 🔍 Business Intelligence")
    
    # Simulador de cenários
    st.markdown("### 🎯 Simulador de Cenários")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 💰 Simulação Financeira")
        
        # Parâmetros da simulação
        fee_increase = st.slider("Aumento da Mensalidade (%)", 0, 30, 10)
        evasion_rate = st.slider("Taxa de Evasão Estimada (%)", 0, 20, 5)
        
        # Cálculos da simulação
        current_revenue = financial_df[financial_df['payment_status'] == 'Pago']['monthly_fee'].sum()
        
        # Receita com aumento
        new_revenue = current_revenue * (1 + fee_increase/100)
        
        # Receita com evasão
        students_remaining = len(students_df) * (1 - evasion_rate/100)
        final_revenue = new_revenue * (students_remaining / len(students_df))
        
        revenue_impact = final_revenue - current_revenue
        
        st.metric("Receita Atual", f"R$ {current_revenue:,.0f}")
        st.metric("Receita Projetada", f"R$ {final_revenue:,.0f}", f"R$ {revenue_impact:,.0f}")
        
        if revenue_impact > 0:
            st.success(f"✅ Impacto positivo de R$ {revenue_impact:,.0f}")
        else:
            st.error(f"❌ Impacto negativo de R$ {abs(revenue_impact):,.0f}")
    
    with col2:
        st.markdown("#### 📚 Simulação Acadêmica")
        
        # Parâmetros acadêmicos
        investment_education = st.slider("Investimento em Educação (%)", 0, 50, 20)
        expected_improvement = st.slider("Melhoria Esperada na Nota", 0.0, 2.0, 0.5, 0.1)
        
        # Projeções acadêmicas
        current_avg = kpis['avg_grade']
        projected_avg = min(10.0, current_avg + expected_improvement)
        
        # Taxa de aprovação projetada
        current_approval = (academic_df['grade'] >= 6.0).mean() * 100
        projected_approval = min(100, current_approval + (expected_improvement * 10))
        
        st.metric("Média Atual", f"{current_avg:.1f}")
        st.metric("Média Projetada", f"{projected_avg:.1f}", f"+{expected_improvement:.1f}")
        st.metric("Taxa de Aprovação Projetada", f"{projected_approval:.1f}%", f"+{projected_approval - current_approval:.1f}%")
    
    # Insights automáticos
    st.markdown("### 💡 Insights Automáticos")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Insight de performance
        best_segment = academic_df.groupby('segment')['grade'].mean().idxmax()
        best_avg = academic_df.groupby('segment')['grade'].mean().max()
        
        st.markdown(f"""
        <div class="alert-premium success">
            <div class="alert-title">🏆 Melhor Performance</div>
            <p><strong>{best_segment}</strong> tem a melhor média: {best_avg:.1f}</p>
            <p><strong>Recomendação:</strong> Replicar metodologia nos outros segmentos</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Insight financeiro
        most_defaulting = financial_df[financial_df['payment_status'] == 'Inadimplente']['segment'].value_counts()
        if not most_defaulting.empty:
            worst_segment = most_defaulting.index[0]
            
            st.markdown(f"""
            <div class="alert-premium warning">
                <div class="alert-title">💰 Atenção Financeira</div>
                <p><strong>{worst_segment}</strong> tem maior inadimplência</p>
                <p><strong>Ação:</strong> Revisar política de cobrança</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col3:
        # Insight operacional
        occupancy_rate = (len(students_df) / 1000) * 100  # Assumindo capacidade de 1000
        
        if occupancy_rate < 80:
            st.markdown(f"""
            <div class="alert-premium warning">
                <div class="alert-title">🎯 Oportunidade</div>
                <p>Ocupação em {occupancy_rate:.1f}%</p>
                <p><strong>Potencial:</strong> {1000 - len(students_df)} novas vagas</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="alert-premium success">
                <div class="alert-title">🏫 Ótima Ocupação</div>
                <p>Taxa de {occupancy_rate:.1f}%</p>
                <p><strong>Status:</strong> Capacidade otimizada</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Exportação de relatórios
    st.markdown("### 📊 Relatórios Executivos")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📋 Relatório Acadêmico Completo", type="primary"):
            st.balloons()
            st.success("📊 Relatório acadêmico gerado e enviado!")
    
    with col2:
        if st.button("💰 Relatório Financeiro Detalhado"):
            st.success("💰 Relatório financeiro exportado!")
    
    with col3:
        if st.button("📈 Dashboard Executivo PDF"):
            st.success("📈 Dashboard executivo em PDF criado!")

if __name__ == "__main__":
    main()
