import dash
from dash import dcc, html, Input, Output, State
import plotly.express as px
import pandas as pd
import requests
from io import BytesIO

# رابط الملف (يمكن تغييره إلى مسار ملف محلي إذا لزم الأمر)
file_url = "https://docs.google.com/spreadsheets/d/1jfmKtvJheeTtEsmjE88zWomQteid2NBn/export?format=xlsx"

# تنزيل الملف من الرابط (إذا كان الملف محليًا، استخدم المسار بدلًا من file_url)
try:
    response = requests.get(file_url)
    response.raise_for_status()  # التحقق من أن الطلب نجح
    file_content = BytesIO(response.content)  # تحويل المحتوى إلى BytesIO
    df = pd.read_excel(file_content)  # قراءة الملف
except Exception as e:
    print(f"حدث خطأ أثناء قراءة الملف: {e}")
    exit()

# التحقق من أن DataFrame ليس فارغًا
if not df.empty:
    # إعادة تسمية الأعمدة
    df = df.rename(columns={
        'السنة': 'السنة',
        'الدولة': 'الدولة',
        'تطوير الحكومة الالكترونية': 'تطوير الحكومة الالكترونية',
        'الخدمات الالكترونية': 'الخدمات الالكترونية',
        'البنية التحتية للاتصالات': 'البنية التحتية للاتصالات',
        'راس المال البشري': 'راس المال البشري',
        'المؤسسات': 'المؤسسات',
        'البنية التحتية ': 'البنية التحتية',  # إعادة تسمية العمود بإزالة المسافة
        'التعليم/ القوى العاملة': 'التعليم/ القوى العاملة',
        'الحكومة الالكترونية': 'الحكومة الالكترونية',
        'الابتكار': 'الابتكار',
        'الجهوزية والمعرفة التكنولوجية': 'الجهوزية والمعرفة التكنولوجية',
        'تطور الاسلوب/بيئة العمل': 'بيئة العمل',  # تغيير النص هنا
        'نمو السوق المالي': 'نمو السوق المالي',
        'التنمية المستدامة': 'التنمية المستدامة',
        'الاقتصاد الرقمي': 'الاقتصاد الرقمي',
        'flg': 'flg'
    })

else:
    print("لا يمكن إعادة تسمية الأعمدة لأن DataFrame فارغ.")

# تنظيف البيانات
if not df.empty:
    df['السنة'] = df['السنة'].dropna().astype(int)
    df['الدولة'] = df['الدولة'].dropna().astype(str)
    df['تطوير الحكومة الالكترونية'] = df['تطوير الحكومة الالكترونية'].dropna().astype(float)
    df['الخدمات الالكترونية'] = df['الخدمات الالكترونية'].dropna().astype(float)
    df['البنية التحتية للاتصالات'] = df['البنية التحتية للاتصالات'].dropna().astype(float)
    df['راس المال البشري'] = df['راس المال البشري'].dropna().astype(float)
    df['المؤسسات'] = df['المؤسسات'].dropna().astype(float)
    df['التعليم/ القوى العاملة'] = df['التعليم/ القوى العاملة'].dropna().astype(float)
    df['الحكومة الالكترونية'] = df['الحكومة الالكترونية'].dropna().astype(float)
    df['الابتكار'] = df['الابتكار'].dropna().astype(float)
    df['الجهوزية والمعرفة التكنولوجية'] = df['الجهوزية والمعرفة التكنولوجية'].dropna().astype(float)
    df['بيئة العمل'] = df['بيئة العمل'].dropna().astype(float)  # تغيير النص هنا
    df['نمو السوق المالي'] = df['نمو السوق المالي'].dropna().astype(float)
    df['التنمية المستدامة'] = df['التنمية المستدامة'].dropna().astype(float)
    df['الاقتصاد الرقمي'] = df['الاقتصاد الرقمي'].dropna().astype(float)

    # التحقق من وجود عمود 'البنية التحتية'
    if 'البنية التحتية' in df.columns:
        df['البنية التحتية'] = df['البنية التحتية'].dropna().astype(float)
    else:
        print("تحذير: العمود 'البنية التحتية' غير موجود في البيانات.")
else:
    print("لا يمكن تنظيف البيانات لأن DataFrame فارغ.")

# دالة لتحديد التقييم
def get_rating(value, indicator):
    if indicator == 'تطوير الحكومة الالكترونية':
        if value > 0.75:
            return "مرتفع جدًا", "#4CAF50"  # أخضر
        elif value > 0.50:
            return "مرتفع", "#FFEB3B"  # أصفر
        elif value > 0.25:
            return "متوسط", "#FF9800"  # برتقالي
        else:
            return "منخفض", "#F44336"  # أحمر
    elif indicator == 'الاقتصاد الرقمي':
        if value > 0.75:
            return "مرتفع جدًا", "#4CAF50"  # أخضر
        elif value > 0.50:
            return "مرتفع", "#FFEB3B"  # أصفر
        elif value > 0.25:
            return "متوسط", "#FF9800"  # برتقالي
        else:
            return "منخفض", "#F44336"  # أحمر

# تطبيق الدالة على البيانات
df['تقييم الحكومة الالكترونية'] = df['تطوير الحكومة الالكترونية'].apply(lambda x: get_rating(x, 'تطوير الحكومة الالكترونية')[0])
df['لون الحكومة الالكترونية'] = df['تطوير الحكومة الالكترونية'].apply(lambda x: get_rating(x, 'تطوير الحكومة الالكترونية')[1])

df['تقييم الاقتصاد الرقمي'] = df['الاقتصاد الرقمي'].apply(lambda x: get_rating(x, 'الاقتصاد الرقمي')[0])
df['لون الاقتصاد الرقمي'] = df['الاقتصاد الرقمي'].apply(lambda x: get_rating(x, 'الاقتصاد الرقمي')[1])

# إنشاء تطبيق Dash
app = dash.Dash(__name__)
# تشغيل الخادم على المنفذ 8052
if __name__ == "__main__":
    app.run_server(port=8052, use_reloader=False)
# تصميم واجهة التطبيق
app.layout = html.Div(style={
    'background': 'linear-gradient(135deg, #001f3f, #003366)',  # تدرج لوني من الأزرق الداكن إلى الأزرق الأغمق
    'height': '100vh',
    'width': '100%',
    'position': 'fixed',
    'top': '0',
    'left': '0',
    'z-index': '-1',
    'color': '#FFFFFF',  # لون النص الأساسي (أبيض)
    'overflow-y': 'scroll',
    'direction': 'rtl',
    'font-family': 'Cairo, sans-serif'  # استخدام خط Cairo
}, children=[
    html.Div([
        html.H2("المؤشرات الدولية حول ليبيا", style={
            'text-align': 'right',
            'font-family': 'Cairo',
            'color': '#FFFFFF',  # لون النص (أبيض)
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
            'color': '#2C3E50',  # لون النص الداخلي (غامق)
            'background-color': 'rgba(255, 255, 255, 0.9)',  # خلفية شبه شفافة (بيضاء)
            'border-radius': '10px',
            'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)',
            'margin-right': '20px'
        }),
        html.Div([
            html.Label("اختر السنة", style={
                'font-family': 'Cairo',
                'color': '#2C3E50',  # لون النص (أبيض)
                'text-align': 'right',
                'display': 'block',
                'margin-bottom': '10px',
                'font-size': '18px',
                'font-weight': 'bold'
            }),
            dcc.Dropdown(
                id='year-filter',
                options=[{'label': year, 'value': year} for year in df['السنة'].unique()],
                value=None,
                multi=True,
                clearable=True,
                style={
                    'width': '100%',
                    'font-family': 'Cairo',
                    'margin-bottom': '20px',
                    'backgroundColor': 'rgba(255, 255, 255, 0.9)',  # خلفية شبه شفافة (بيضاء)
                    'color': '#2C3E50',  # لون النص (غامق)
                    'border-radius': '5px',
                    'border': '1px solid #ddd'
                }
            ),
            html.Label("اختر الدولة", style={
                'font-family': 'Cairo',
                'color': '#2C3E50',  # لون النص (أبيض)
                'text-align': 'right',
                'display': 'block',
                'margin-bottom': '10px',
                'font-size': '18px',
                'font-weight': 'bold'
            }),
            dcc.Dropdown(
                id='country-filter',
                options=[{'label': country, 'value': country} for country in df['الدولة'].unique()],
                value=None,
                multi=True,
                clearable=True,
                style={
                    'width': '100%',
                    'font-family': 'Cairo',
                    'backgroundColor': 'rgba(255, 255, 255, 0.9)',  # خلفية شبه شفافة (بيضاء)
                    'color': '#2C3E50',  # لون النص (غامق)
                    'border-radius': '5px',
                    'border': '1px solid #ddd'
                }
            ),
            html.Label("اختر نوع العرض", style={
                'font-family': 'Cairo',
                'color': '#2C3E50',  # لون النص (أبيض)
                'text-align': 'right',
                'display': 'block',
                'margin-bottom': '10px',
                'font-size': '18px',
                'font-weight': 'bold'
            }),
            dcc.RadioItems(
                id='chart-type',
                options=[
                    {'label': 'عرض مؤشر تطوير الحكومة الإلكترونية والاقتصاد الرقمي', 'value': 'bar'},
                    {'label': 'عرض المؤشرات الفرعية لمؤشر تطوير الحكومة الإلكترونية', 'value': 'pie'}, 
                    {'label': 'عرض المؤشرات الفرعية لمؤشر الاقتصاد الرقمي', 'value': 'donut'}
                ],
                value=None,
                style={
                    'font-family': 'Cairo',
                    'color': '#2C3E50',  # لون النص (أبيض)
                    'font-size': '16px'
                }
            ),
            html.Button(
                '🔄',
                id='refresh-button',
                style={
                    'font-family': 'Cairo',
                    'color': '#2C3E50',  # لون النص (غامق)
                    'background-color': 'rgba(255, 255, 255, 0.9)',  # خلفية شبه شفافة (بيضاء)
                    'border': '1px solid #ddd',
                    'border-radius': '50%',
                    'padding': '10px',
                    'width': '50px',
                    'height': '50px',
                    'margin-top': '20px',
                    'cursor': 'pointer',
                    'display': 'flex',
                    'align-items': 'center',
                    'justify-content': 'center',
                    'font-size': '18px',
                    'transition': 'background-color 0.3s ease'
                }
            ),
        ], style={
            'width': '20%',
            'padding': '20px',
            'background-color': 'rgba(255, 255, 255, 0.9)',  # خلفية شبه شفافة (بيضاء)
            'border-left': '1px solid #ddd',
            'height': '70vh',
            'overflow-y': 'auto',
            'order': 1,
            'color': '#2C3E50',  # لون النص (غامق)
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

# تعريف callback لتحديث المحتوى
@app.callback(
    Output('content', 'children'),
    [Input('year-filter', 'value'),
     Input('country-filter', 'value'),
     Input('chart-type', 'value'),
     Input('refresh-button', 'n_clicks')]
)
def update_content(selected_years, selected_countries, chart_type, n_clicks):
    if n_clicks is None and not selected_years and not selected_countries:
        return html.Div([
            html.H3("تعريف المؤشرات", style={
                'text-align': 'right',
                'font-family': 'Cairo',
                'color': '#2C3E50',  # لون النص الداخلي (غامق)
                'font-size': '24px',
                'font-weight': 'bold',
                'margin-bottom': '20px'
            }),
            html.P("""
                مؤشر تطوير الحكومة الإلكترونية: يقيس مدى تقدم الحكومة في استخدام التقنيات الرقمية لتقديم الخدمات العامة.
            """, style={
                'text-align': 'right',
                'font-family': 'Cairo',
                'color': '#2C3E50',  # لون النص الداخلي (غامق)
                'font-size': '16px',
                'line-height': '1.6'
            }),
            html.P("""
                مؤشر الاقتصاد الرقمي: يقيس مدى تطور الاقتصاد الرقمي في الدولة بناءً على عدة معايير مثل البنية التحتية الرقمية والاستثمارات التكنولوجية.
            """, style={
                'text-align': 'right',
                'font-family': 'Cairo',
                'color': '#2C3E50',  # لون النص الداخلي (غامق)
                'font-size': '16px',
                'line-height': '1.6'
            }),
        ])

    if selected_years and selected_countries:
        filtered_df = df[(df['السنة'].isin(selected_years)) & 
                         (df['الدولة'].isin(selected_countries))]
    else:
        filtered_df = pd.DataFrame()

    if filtered_df.empty:
        return html.Div("لا توجد بيانات متاحة للعرض بناءً على الفلاتر المحددة.", style={
            'text-align': 'right',
            'font-family': 'Cairo',
            'color': '#2C3E50',  # لون النص الداخلي (غامق)
            'font-size': '18px',
            'font-weight': 'bold'
        })

    graphs = []

    if chart_type == 'pie':
        if isinstance(selected_years, list) and isinstance(selected_countries, list):
            if len(selected_years) == 1 and len(selected_countries) == 1:
                # تحقق من وجود الأعمدة المطلوبة
                required_columns = [
                    'الخدمات الالكترونية', 'البنية التحتية للاتصالات', 'راس المال البشري'
                ]
                
                if all(column in df.columns for column in required_columns):
                    # إنشاء DataFrame للبيانات
                    pie_data = pd.DataFrame({
                        'المؤشر': [
                            'الخدمات الالكترونية', 'البنية التحتية للاتصالات', 'راس المال البشري'
                        ],
                        'القيمة': [
                            filtered_df['الخدمات الالكترونية'].values[0],
                            filtered_df['البنية التحتية للاتصالات'].values[0],
                            filtered_df['راس المال البشري'].values[0]
                        ]
                    })

                    # إنشاء عنوان ديناميكي يعكس الدولة والسنة
                    title = f"المؤشرات الفرعية لتطوير الحكومة الإلكترونية ({selected_countries[0]} - {selected_years[0]})"

                    # إنشاء المخطط الدائري
                    pie_fig = px.pie(
                        pie_data,
                        values='القيمة',
                        names='المؤشر',
                        title=title,
                        labels={'القيمة': 'القيمة', 'المؤشر': 'المؤشر'},
                        hover_data={'القيمة': ':.2f'},
                        color_discrete_sequence=px.colors.qualitative.Pastel  # ألوان هادئة
                    )

                    # تحسين إعدادات التخطيط
                    pie_fig.update_traces(
                        textinfo='percent+label',  # عرض النسبة المئوية والتسمية
                        textposition='inside',  # وضع التسميات داخل الشرائح
                        marker=dict(line=dict(color='white', width=2))  # إضافة حدود بيضاء للشرائح
                    )

                    pie_fig.update_layout(
                        font_family='Cairo',
                        title_font_size=20,
                        title={'text': title, 'x': 0.5, 'font': {'color': '#2C3E50'}},  # لون النص الداخلي (غامق)
                        plot_bgcolor='rgba(255, 255, 255, 0.9)',  # خلفية شبه شفافة (بيضاء)
                        paper_bgcolor='rgba(255, 255, 255, 0.9)',  # خلفية شبه شفافة (بيضاء)
                        font={'color': '#2C3E50'},  # لون النص الداخلي (غامق)
                        legend={'font': {'color': '#2C3E50'}},  # لون نص وسيلة الإيضاح
                        showlegend=True  # إظهار وسيلة الإيضاح
                    )
                    graphs.append(dcc.Graph(
                        id='pie-chart',
                        figure=pie_fig,
                        style={
                            'width': '100%',
                            'display': 'inline-block',
                            'backgroundColor': 'rgba(255, 255, 255, 0.9)',  # خلفية شبه شفافة (بيضاء)
                            'color': '#2C3E50',  # لون النص الداخلي (غامق)
                            'border-radius': '10px',
                            'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)'
                        }
                    ))
                else:
                    graphs.append(html.Div("بعض الأعمدة المطلوبة غير موجودة في البيانات.", style={
                        'text-align': 'right',
                        'font-family': 'Cairo',
                        'color': '#2C3E50',  # لون النص الداخلي (غامق)
                        'font-size': '18px',
                        'font-weight': 'bold'
                    }))
            else:
                graphs.append(html.Div("يجب اختيار سنة واحدة ودولة واحدة لعرض المؤشرات الفرعية لتطوير الحكومة الإلكترونية.", style={
                    'text-align': 'right',
                    'font-family': 'Cairo',
                    'color': '#2C3E50',  # لون النص الداخلي (غامق)
                    'font-size': '18px',
                    'font-weight': 'bold'
                }))
        else:
            graphs.append(html.Div("يجب اختيار سنة واحدة ودولة واحدة لعرض المؤشرات الفرعية لتطوير الحكومة الإلكترونية.", style={
                'text-align': 'right',
                'font-family': 'Cairo',
                'color': '#2C3E50',  # لون النص الداخلي (غامق)
                'font-size': '18px',
                'font-weight': 'bold'
            }))
    elif chart_type == 'donut':
        if isinstance(selected_years, list) and isinstance(selected_countries, list):
            if len(selected_years) == 1 and len(selected_countries) == 1:
                # تحقق من وجود الأعمدة المطلوبة
                required_columns = [
                    'المؤسسات', 'البنية التحتية', 'التعليم/ القوى العاملة',
                    'الحكومة الالكترونية', 'الابتكار', 'الجهوزية والمعرفة التكنولوجية',
                    'بيئة العمل', 'نمو السوق المالي', 'التنمية المستدامة'
                ]
                
                if all(column in df.columns for column in required_columns):
                    # إنشاء DataFrame للبيانات
                    donut_data = pd.DataFrame({
                        'المؤشر': [
                            'المؤسسات', 'البنية التحتية', 'التعليم/ القوى العاملة',
                            'الحكومة الالكترونية', 'الابتكار', 'الجهوزية والمعرفة التكنولوجية',
                            'بيئة العمل', 'نمو السوق المالي', 'التنمية المستدامة'
                        ],
                        'القيمة': [
                            filtered_df['المؤسسات'].values[0],
                            filtered_df['البنية التحتية'].values[0],
                            filtered_df['التعليم/ القوى العاملة'].values[0],
                            filtered_df['الحكومة الالكترونية'].values[0],
                            filtered_df['الابتكار'].values[0],
                            filtered_df['الجهوزية والمعرفة التكنولوجية'].values[0],
                            filtered_df['بيئة العمل'].values[0],
                            filtered_df['نمو السوق المالي'].values[0],
                            filtered_df['التنمية المستدامة'].values[0]
                            
                        ]
                    })

                    # التحقق من وجود بيانات صالحة
                    if donut_data['القيمة'].sum() > 0:  # إذا كانت هناك بيانات صالحة
                        # إنشاء عنوان ديناميكي يعكس الدولة والسنة
                        title = f"المؤشرات الفرعية للاقتصاد الرقمي ({selected_countries[0]} - {selected_years[0]})"

                        # إنشاء المخطط الدائري مع فجوة في المنتصف (دونت)
                        donut_fig = px.pie(
                            donut_data,
                            values='القيمة',
                            names='المؤشر',
                            title=title,
                            labels={'القيمة': 'القيمة', 'المؤشر': 'المؤشر'},
                            hover_data={'القيمة': ':.2f'},
                            hole=0.4,  # إضافة فجوة في المنتصف لإنشاء مخطط دونت
                            color_discrete_sequence=px.colors.qualitative.Pastel  # ألوان هادئة
                        )

                        # تحسين إعدادات التخطيط
                        donut_fig.update_traces(
                            textinfo='percent+label',  # عرض النسبة المئوية والتسمية
                            textposition='inside',  # وضع التسميات داخل الشرائح
                            marker=dict(line=dict(color='white', width=2))  # إضافة حدود بيضاء للشرائح
                        )

                        donut_fig.update_layout(
                            font_family='Cairo',
                            title_font_size=20,
                            title={'text': title, 'x': 0.5, 'font': {'color': '#2C3E50'}},  # لون النص الداخلي (غامق)
                            plot_bgcolor='rgba(255, 255, 255, 0.9)',  # خلفية شبه شفافة (بيضاء)
                            paper_bgcolor='rgba(255, 255, 255, 0.9)',  # خلفية شبه شفافة (بيضاء)
                            font={'color': '#2C3E50'},  # لون النص الداخلي (غامق)
                            legend={'font': {'color': '#2C3E50'}},  # لون نص وسيلة الإيضاح
                            showlegend=True  # إظهار وسيلة الإيضاح
                        )
                        graphs.append(dcc.Graph(
                            id='donut-chart',
                            figure=donut_fig,
                            style={
                                'width': '100%',
                                'display': 'inline-block',
                                'backgroundColor': 'rgba(255, 255, 255, 0.9)',  # خلفية شبه شفافة (بيضاء)
                                'color': '#2C3E50',  # لون النص الداخلي (غامق)
                                'border-radius': '10px',
                                'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)'
                            }
                        ))
                    else:
                        # عرض رسالة بديلة إذا لم تكن هناك بيانات صالحة
                        graphs.append(html.Div("لا توجد بيانات متاحة للعرض لمؤشر الاقتصاد الرقمي للسنوات المحددة (2018، 2020، 2022).", style={
                            'text-align': 'right',
                            'font-family': 'Cairo',
                            'color': '#2C3E50',  # لون النص الداخلي (غامق)
                            'font-size': '18px',
                            'font-weight': 'bold'
                        }))
                else:
                    graphs.append(html.Div("بعض الأعمدة المطلوبة غير موجودة في البيانات.", style={
                        'text-align': 'right',
                        'font-family': 'Cairo',
                        'color': '#2C3E50',  # لون النص الداخلي (غامق)
                        'font-size': '18px',
                        'font-weight': 'bold'
                    }))
            else:
                graphs.append(html.Div("يجب اختيار سنة واحدة ودولة واحدة لعرض المؤشرات الفرعية للاقتصاد الرقمي.", style={
                    'text-align': 'right',
                    'font-family': 'Cairo',
                    'color': '#2C3E50',  # لون النص الداخلي (غامق)
                    'font-size': '18px',
                    'font-weight': 'bold'
                }))
        else:
            graphs.append(html.Div("يجب اختيار سنة واحدة ودولة واحدة لعرض المؤشرات الفرعية للاقتصاد الرقمي.", style={
                'text-align': 'right',
                'font-family': 'Cairo',
                'color': '#2C3E50',  # لون النص الداخلي (غامق)
                'font-size': '18px',
                'font-weight': 'bold'
            }))
    elif chart_type == 'bar':
        if not filtered_df[['الدولة', 'تطوير الحكومة الالكترونية']].dropna().empty:
            e_gov_fig = px.bar(
                filtered_df,
                x='الدولة',
                y='تطوير الحكومة الالكترونية',
                title='مؤشر تطوير الحكومة الإلكترونية',
                labels={'تطوير الحكومة الالكترونية': 'المؤشر', 'الدولة': 'الدولة', 'السنة': 'السنة'},
                hover_data=['السنة'],
                orientation='v',
                text_auto=True,
                color='تقييم الحكومة الالكترونية',  # استخدام التقييم كلون
                color_discrete_map={
                    "مرتفع جدًا": "#4CAF50",  # أخضر
                    "مرتفع": "#FFEB3B",  # أصفر
                    "متوسط": "#FF9800",  # برتقالي
                    "منخفض": "#F44336"  # أحمر
                }
            )

            e_gov_fig.update_layout(
                font_family='Cairo',
                title_font_size=20,
                title={'text': 'مؤشر تطوير الحكومة الإلكترونية', 'x': 0.5, 'font': {'color': '#2C3E50'}},  # لون النص الداخلي (غامق)
                plot_bgcolor='rgba(255, 255, 255, 0.9)',  # خلفية شبه شفافة (بيضاء)
                paper_bgcolor='rgba(255, 255, 255, 0.9)',  # خلفية شبه شفافة (بيضاء)
                font={'color': '#2C3E50'},  # لون النص الداخلي (غامق)
                xaxis={'color': '#2C3E50'},  # لون النص الداخلي (غامق)
                yaxis={'color': '#2C3E50'}  # لون النص الداخلي (غامق)
            )
            graphs.append(dcc.Graph(
                id='e-gov-graph',
                figure=e_gov_fig,
                style={
                    'width': '48%',
                    'display': 'inline-block',
                    'backgroundColor': 'rgba(255, 255, 255, 0.9)',  # خلفية شبه شفافة (بيضاء)
                    'color': '#2C3E50',  # لون النص الداخلي (غامق)
                    'border-radius': '10px',
                    'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)'
                }
            ))

        if not filtered_df[['الدولة', 'الاقتصاد الرقمي']].dropna().empty:
            digital_economy_fig = px.bar(
                filtered_df,
                x='الدولة',
                y='الاقتصاد الرقمي',
                title='مؤشر الاقتصاد الرقمي',
                labels={'الاقتصاد الرقمي': 'المؤشر', 'الدولة': 'الدولة', 'السنة': 'السنة'},
                hover_data=['السنة'],
                orientation='v',
                text_auto=True,
                color='تقييم الاقتصاد الرقمي',  # استخدام التقييم كلون
                color_discrete_map={
                    "مرتفع جدًا": "#4CAF50",  # أخضر
                    "مرتفع": "#FFEB3B",  # أصفر
                    "متوسط": "#FF9800",  # برتقالي
                    "منخفض": "#F44336"  # أحمر
                }
            )

            digital_economy_fig.update_layout(
                font_family='Cairo',
                title_font_size=20,
                title={'text': 'مؤشر الاقتصاد الرقمي', 'x': 0.5, 'font': {'color': '#2C3E50'}},  # لون النص الداخلي (غامق)
                plot_bgcolor='rgba(255, 255, 255, 0.9)',  # خلفية شبه شفافة (بيضاء)
                paper_bgcolor='rgba(255, 255, 255, 0.9)',  # خلفية شبه شفافة (بيضاء)
                font={'color': '#2C3E50'},  # لون النص الداخلي (غامق)
                xaxis={'color': '#2C3E50'},  # لون النص الداخلي (غامق)
                yaxis={'color': '#2C3E50'}  # لون النص الداخلي (غامق)
            )
            graphs.append(dcc.Graph(
                id='digital-economy-graph',
                figure=digital_economy_fig,
                style={
                    'width': '48%',
                    'display': 'inline-block',
                    'backgroundColor': 'rgba(255, 255, 255, 0.9)',  # خلفية شبه شفافة (بيضاء)
                    'color': '#2C3E50',  # لون النص الداخلي (غامق)
                    'border-radius': '10px',
                    'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)'
                }
            ))
        else:
            # عرض رسالة بديلة إذا لم تكن هناك بيانات للاقتصاد الرقمي
            graphs.append(html.Div("لا توجد بيانات متاحة للعرض لمؤشر الاقتصاد الرقمي للسنوات المحددة (2018، 2020، 2022).", style={
                'text-align': 'right',
                'font-family': 'Cairo',
                'color': '#2C3E50',  # لون النص الداخلي (غامق)
                'font-size': '18px',
                'font-weight': 'bold'
            }))

    return html.Div(graphs)

# تعريف callback لإعادة تعيين الفلاتر وزر الراديو
@app.callback(
    [Output('year-filter', 'value'),
     Output('country-filter', 'value'),
     Output('chart-type', 'value')],
    [Input('refresh-button', 'n_clicks')]
)
def reset_filters(n_clicks):
    if n_clicks:
        return None, None, None
    return dash.no_update, dash.no_update, dash.no_update
server = app.server  # هذا السطر مهم لتشغيل التطبيق على PythonAnywhere
# تشغيل التطبيق
if __name__ == '__main__':
    app.run_server(debug=False)
