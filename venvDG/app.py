import dash
from dash import dcc, html, Input, Output, State
import plotly.express as px
import pandas as pd
import requests
from io import BytesIO

# ==============================================
# 1. تحميل البيانات
# ==============================================

def load_data():
    """
    تحميل البيانات من رابط الملف الخارجي.
    يتم تحميل البيانات مرة واحدة عند بدء التشغيل.
    """
    file_url = "https://docs.google.com/spreadsheets/d/1jfmKtvJheeTtEsmjE88zWomQteid2NBn/export?format=xlsx"
    
    try:
        response = requests.get(file_url)
        response.raise_for_status()  # التحقق من نجاح الطلب
        file_content = BytesIO(response.content)  # تحويل المحتوى إلى BytesIO
        df = pd.read_excel(file_content)  # قراءة الملف
        return df
    except Exception as e:
        print(f"حدث خطأ أثناء قراءة الملف: {e}")
        return pd.DataFrame()  # إرجاع DataFrame فارغ في حالة الخطأ

# تحميل البيانات مرة واحدة عند بدء التشغيل
df = load_data()

# إذا فشل تحميل البيانات، يتم إيقاف التطبيق
if df.empty:
    print("لا يمكن المتابعة بسبب فشل تحميل البيانات.")
    exit()

# ==============================================
# 2. تنظيف البيانات
# ==============================================

def clean_data(df):
    """
    تنظيف البيانات وإعادة تسمية الأعمدة.
    """
    if df.empty:
        print("DataFrame فارغ، لا يمكن تنظيف البيانات.")
        return df

    # إعادة تسمية الأعمدة
    df = df.rename(columns={
        'السنة': 'السنة',
        'الدولة': 'الدولة',
        'تطوير الحكومة الالكترونية': 'تطوير الحكومة الالكترونية',
        'الخدمات الالكترونية': 'الخدمات الالكترونية',
        'البنية التحتية للاتصالات': 'البنية التحتية للاتصالات',
        'راس المال البشري': 'راس المال البشري',
        'المؤسسات': 'المؤسسات',
        'البنية التحتية ': 'البنية التحتية',  # إزالة المسافة الزائدة
        'التعليم/ القوى العاملة': 'التعليم/ القوى العاملة',
        'الحكومة الالكترونية': 'الحكومة الالكترونية',
        'الابتكار': 'الابتكار',
        'الجهوزية والمعرفة التكنولوجية': 'الجهوزية والمعرفة التكنولوجية',
        'تطور الاسلوب/بيئة العمل': 'بيئة العمل',
        'نمو السوق المالي': 'نمو السوق المالي',
        'التنمية المستدامة': 'التنمية المستدامة',
        'الاقتصاد الرقمي': 'الاقتصاد الرقمي',
        'flg': 'flg'
    })

    # تنظيف الأعمدة
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].dropna().astype(str)
        elif df[col].dtype == 'float64' or df[col].dtype == 'int64':
            df[col] = df[col].dropna().astype(float)

    return df

# تنظيف البيانات
df = clean_data(df)

# ==============================================
# 3. دالة لتحديد التقييم
# ==============================================

def get_rating(value, indicator):
    """
    تحديد التقييم بناءً على القيمة والمؤشر.
    """
    if indicator == 'تطوير الحكومة الالكترونية' or indicator == 'الاقتصاد الرقمي':
        if value > 0.75:
            return "مرتفع جدًا", "#4CAF50"  # أخضر
        elif value > 0.50:
            return "مرتفع", "#FFEB3B"  # أصفر
        elif value > 0.25:
            return "متوسط", "#FF9800"  # برتقالي
        else:
            return "منخفض", "#F44336"  # أحمر
    return None, None

# تطبيق الدالة على البيانات
df['تقييم الحكومة الالكترونية'] = df['تطوير الحكومة الالكترونية'].apply(lambda x: get_rating(x, 'تطوير الحكومة الالكترونية')[0])
df['لون الحكومة الالكترونية'] = df['تطوير الحكومة الالكترونية'].apply(lambda x: get_rating(x, 'تطوير الحكومة الالكترونية')[1])

df['تقييم الاقتصاد الرقمي'] = df['الاقتصاد الرقمي'].apply(lambda x: get_rating(x, 'الاقتصاد الرقمي')[0])
df['لون الاقتصاد الرقمي'] = df['الاقتصاد الرقمي'].apply(lambda x: get_rating(x, 'الاقتصاد الرقمي')[1])

# ==============================================
# 4. إنشاء تطبيق Dash
# ==============================================

app = dash.Dash(__name__)

# ==============================================
# 5. تصميم واجهة التطبيق
# ==============================================

app.layout = html.Div(style={
    'background': 'linear-gradient(135deg, #001f3f, #003366)',
    'height': '100vh',
    'width': '100%',
    'color': '#FFFFFF',
    'overflow-y': 'scroll',
    'direction': 'rtl',
    'font-family': 'Cairo, sans-serif'
}, children=[
    html.Div([
        html.H2("المؤشرات الدولية حول ليبيا", style={
            'text-align': 'right',
            'font-size': '28px',
            'font-weight': 'bold',
            'margin-bottom': '20px',
            'padding-top': '40px'
        }),
        html.Img(src='/assets/logo.png', style={'height': '200px', 'margin-right': '10px'}),
    ], style={
        'display': 'flex',
        'align-items': 'center',
        'justify-content': 'flex-end',
        'flex-direction': 'row-reverse',
        'margin-bottom': '20px',
        'padding': '0 20px'
    }),
    html.Div([
        html.Div(id='content', style={
            'width': '80%',
            'padding': '20px',
            'height': '70vh',
            'overflow-y': 'auto',
            'order': 2,
            'color': '#2C3E50',
            'background-color': 'rgba(255, 255, 255, 0.9)',
            'border-radius': '10px',
            'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)',
            'margin-right': '20px'
        }),
        html.Div([
            html.Label("اختر السنة", style={'font-size': '18px', 'font-weight': 'bold'}),
            dcc.Dropdown(
                id='year-filter',
                options=[{'label': year, 'value': year} for year in df['السنة'].unique()],
                value=None,
                multi=True,
                clearable=True,
                style={'width': '100%', 'margin-bottom': '20px'}
            ),
            html.Label("اختر الدولة", style={'font-size': '18px', 'font-weight': 'bold'}),
            dcc.Dropdown(
                id='country-filter',
                options=[{'label': country, 'value': country} for country in df['الدولة'].unique()],
                value=None,
                multi=True,
                clearable=True,
                style={'width': '100%'}
            ),
            html.Label("اختر نوع العرض", style={'font-size': '18px', 'font-weight': 'bold'}),
            dcc.RadioItems(
                id='chart-type',
                options=[
                    {'label': 'عرض مؤشر تطوير الحكومة الإلكترونية والاقتصاد الرقمي', 'value': 'bar'},
                    {'label': 'عرض المؤشرات الفرعية لتطوير الحكومة الإلكترونية', 'value': 'pie'},
                    {'label': 'عرض المؤشرات الفرعية للاقتصاد الرقمي', 'value': 'donut'}
                ],
                value=None,
                style={'font-size': '16px'}
            ),
            html.Button('🔄', id='refresh-button', style={
                'margin-top': '20px',
                'cursor': 'pointer',
                'font-size': '18px',
                'padding': '10px',
                'border-radius': '50%',
                'background-color': 'rgba(255, 255, 255, 0.9)',
                'border': '1px solid #ddd'
            }),
        ], style={
            'width': '20%',
            'padding': '20px',
            'background-color': 'rgba(255, 255, 255, 0.9)',
            'border-left': '1px solid #ddd',
            'height': '70vh',
            'overflow-y': 'auto',
            'order': 1,
            'border-radius': '10px',
            'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)'
        }),
    ], style={
        'display': 'flex',
        'justify-content': 'space-between',
        'margin-top': '20px',
        'padding': '0 20px',
        'flex-direction': 'row'
    }),
])

# ==============================================
# 6. تعريف Callbacks
# ==============================================

@app.callback(
    Output('content', 'children'),
    [Input('year-filter', 'value'),
     Input('country-filter', 'value'),
     Input('chart-type', 'value'),
     Input('refresh-button', 'n_clicks')]
)
def update_content(selected_years, selected_countries, chart_type, n_clicks):
    try:
        if n_clicks is None and not selected_years and not selected_countries:
            return html.Div([
                html.H3("تعريف المؤشرات", style={'font-size': '24px', 'font-weight': 'bold'}),
                html.P("مؤشر تطوير الحكومة الإلكترونية: يقيس مدى تقدم الحكومة في استخدام التقنيات الرقمية لتقديم الخدمات العامة."),
                html.P("مؤشر الاقتصاد الرقمي: يقيس مدى تطور الاقتصاد الرقمي في الدولة بناءً على عدة معايير مثل البنية التحتية الرقمية والاستثمارات التكنولوجية.")
            ])

        if selected_years and selected_countries:
            filtered_df = df[(df['السنة'].isin(selected_years)) & (df['الدولة'].isin(selected_countries))]
        else:
            filtered_df = pd.DataFrame()

        if filtered_df.empty:
            return html.Div("لا توجد بيانات متاحة للعرض بناءً على الفلاتر المحددة.", style={'font-size': '18px', 'font-weight': 'bold'})

        graphs = []

        if chart_type == 'pie':
            if isinstance(selected_years, list) and isinstance(selected_countries, list):
                if len(selected_years) == 1 and len(selected_countries) == 1:
                    required_columns = ['الخدمات الالكترونية', 'البنية التحتية للاتصالات', 'راس المال البشري']
                    if all(column in df.columns for column in required_columns):
                        pie_data = pd.DataFrame({
                            'المؤشر': required_columns,
                            'القيمة': [filtered_df[col].values[0] for col in required_columns]
                        })
                        pie_fig = px.pie(pie_data, values='القيمة', names='المؤشر', title="المؤشرات الفرعية لتطوير الحكومة الإلكترونية")
                        graphs.append(dcc.Graph(figure=pie_fig))
                    else:
                        graphs.append(html.Div("بعض الأعمدة المطلوبة غير موجودة في البيانات.", style={'font-size': '18px', 'font-weight': 'bold'}))
                else:
                    graphs.append(html.Div("يجب اختيار سنة واحدة ودولة واحدة لعرض المؤشرات الفرعية لتطوير الحكومة الإلكترونية.", style={'font-size': '18px', 'font-weight': 'bold'}))
            else:
                graphs.append(html.Div("يجب اختيار سنة واحدة ودولة واحدة لعرض المؤشرات الفرعية لتطوير الحكومة الإلكترونية.", style={'font-size': '18px', 'font-weight': 'bold'}))

        elif chart_type == 'donut':
            if isinstance(selected_years, list) and isinstance(selected_countries, list):
                if len(selected_years) == 1 and len(selected_countries) == 1:
                    required_columns = ['المؤسسات', 'البنية التحتية', 'التعليم/ القوى العاملة', 'الحكومة الالكترونية', 'الابتكار', 'الجهوزية والمعرفة التكنولوجية', 'بيئة العمل', 'نمو السوق المالي', 'التنمية المستدامة']
                    if all(column in df.columns for column in required_columns):
                        donut_data = pd.DataFrame({
                            'المؤشر': required_columns,
                            'القيمة': [filtered_df[col].values[0] for col in required_columns]
                        })
                        donut_fig = px.pie(donut_data, values='القيمة', names='المؤشر', title="المؤشرات الفرعية للاقتصاد الرقمي", hole=0.4)
                        graphs.append(dcc.Graph(figure=donut_fig))
                    else:
                        graphs.append(html.Div("بعض الأعمدة المطلوبة غير موجودة في البيانات.", style={'font-size': '18px', 'font-weight': 'bold'}))
                else:
                    graphs.append(html.Div("يجب اختيار سنة واحدة ودولة واحدة لعرض المؤشرات الفرعية للاقتصاد الرقمي.", style={'font-size': '18px', 'font-weight': 'bold'}))
            else:
                graphs.append(html.Div("يجب اختيار سنة واحدة ودولة واحدة لعرض المؤشرات الفرعية للاقتصاد الرقمي.", style={'font-size': '18px', 'font-weight': 'bold'}))

        elif chart_type == 'bar':
            if not filtered_df[['الدولة', 'تطوير الحكومة الالكترونية']].dropna().empty:
                e_gov_fig = px.bar(filtered_df, x='الدولة', y='تطوير الحكومة الالكترونية', title='مؤشر تطوير الحكومة الإلكترونية', color='تقييم الحكومة الالكترونية', color_discrete_map={"مرتفع جدًا": "#4CAF50", "مرتفع": "#FFEB3B", "متوسط": "#FF9800", "منخفض": "#F44336"})
                graphs.append(dcc.Graph(figure=e_gov_fig))

            if not filtered_df[['الدولة', 'الاقتصاد الرقمي']].dropna().empty:
                digital_economy_fig = px.bar(filtered_df, x='الدولة', y='الاقتصاد الرقمي', title='مؤشر الاقتصاد الرقمي', color='تقييم الاقتصاد الرقمي', color_discrete_map={"مرتفع جدًا": "#4CAF50", "مرتفع": "#FFEB3B", "متوسط": "#FF9800", "منخفض": "#F44336"})
                graphs.append(dcc.Graph(figure=digital_economy_fig))
            else:
                graphs.append(html.Div("لا توجد بيانات متاحة للعرض لمؤشر الاقتصاد الرقمي.", style={'font-size': '18px', 'font-weight': 'bold'}))

        return html.Div(graphs)

    except Exception as e:
        return html.Div(f"حدث خطأ أثناء تحديث المحتوى: {str(e)}", style={'font-size': '18px', 'font-weight': 'bold'})

# ==============================================
# 7. تشغيل التطبيق
# ==============================================

if __name__ == '__main__':
    app.run_server(debug=True, port=8055, use_reloader=False)
