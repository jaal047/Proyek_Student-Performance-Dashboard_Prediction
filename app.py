import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff

# Styling
st.set_page_config(page_title="Jaya Jaya Institut Dashboard", layout="wide")

# Load Data
data = pd.read_csv('data/data.csv', sep=';')

# Mapping untuk variabel biner
mapping_dict = {
    'Gender': {1: 'Male', 0: 'Female'},
    'Daytime_evening_attendance': {1: 'Daytime', 0: 'Evening'},
    'Displaced': {1: 'Yes', 0: 'No'},
    'Educational_special_needs': {1: 'Yes', 0: 'No'},
    'Debtor': {1: 'Yes', 0: 'No'},
    'Scholarship_holder': {1: 'Yes', 0: 'No'},
    'International': {1: 'Yes', 0: 'No'}
}

# Terapkan mapping ke dataset
for column, mapping in mapping_dict.items():
    data[column] = data[column].map(mapping)

# Definisi fitur numerikal dan kategorikal
numerical_columns = [
    'Application_order', 'Previous_qualification', 'Admission_grade', 'Age_at_enrollment',
    'Curricular_units_1st_sem_credited', 'Curricular_units_1st_sem_enrolled',
    'Curricular_units_1st_sem_evaluations', 'Curricular_units_1st_sem_approved',
    'Curricular_units_1st_sem_grade', 'Curricular_units_1st_sem_without_evaluations',
    'Curricular_units_2nd_sem_credited', 'Curricular_units_2nd_sem_enrolled',
    'Curricular_units_2nd_sem_evaluations', 'Curricular_units_2nd_sem_approved',
    'Curricular_units_2nd_sem_grade', 'Curricular_units_2nd_sem_without_evaluations',
    'Unemployment_rate', 'Inflation_rate', 'GDP'
]

categorical_columns = [
    'Marital_status', 'Application_mode', 'Course', 'Daytime_evening_attendance',
    'Previous_qualification', 'Nacionality', "Mothers_qualification", "Fathers_qualification",
    "Mothers_occupation", "Fathers_occupation", 'Displaced', 'Educational_special_needs',
    'Debtor', 'Tuition_fees_up_to_date', 'Gender', 'Scholarship_holder', 'International'
]

# Sidebar Menu
st.sidebar.title("Jaya Jaya Institut Dashboard")
menu = st.sidebar.selectbox("Pilih Halaman:", ["📊 Business Dashboard", "🔍 Prediction Page"])

# =======================
# 📊 Business Dashboard
# =======================
if menu == "📊 Business Dashboard":
    st.title("📊 Business Dashboard - Students' Performance")
    
    # Overview Metrics
    st.write("## 🎓 **Overview Metrics**")
    col1, col2, col3, col4 = st.columns(4)
    
    # Total Students
    with col1:
        total_students = len(data)
        st.metric(label="Total Students", value=total_students)
    
    # Dropout Rate
    with col2:
        dropout_rate = (data['Status'].value_counts(normalize=True).get('Dropout', 0)) * 100
        st.metric(label="Dropout Rate (%)", value=f"{dropout_rate:.2f}%")
    
    # Students with Special Educational Needs
    with col3:
        special_needs = data['Educational_special_needs'].value_counts().get('Yes', 0)
        st.metric(label="Special Educational Needs", value=special_needs)
    
    # Total Graduates
    with col4:
        total_graduates = data['Status'].value_counts().get('Graduate', 0)
        st.metric(label="Total Graduates", value=total_graduates)

    st.write("---")
    
    # Mapping Courses
    course_mapping = {
        33: 'Biofuel Production Technologies',
        171: 'Animation and Multimedia Design',
        8014: 'Social Service (evening attendance)',
        9003: 'Agronomy',
        9070: 'Communication Design',
        9085: 'Veterinary Nursing',
        9119: 'Informatics Engineering',
        9130: 'Equinculture',
        9147: 'Management',
        9238: 'Social Service',
        9254: 'Tourism',
        9500: 'Nursing',
        9556: 'Oral Hygiene',
        9670: 'Advertising and Marketing Management',
        9773: 'Journalism and Communication',
        9853: 'Basic Education',
        9991: 'Management (evening attendance)'
    }

    # Tambahkan opsi "All Students"
    course_options = ["All Students"] + list(course_mapping.values())
    selected_course = st.selectbox("Pilih Course:", course_options)

    # Filter data berdasarkan pilihan
    if selected_course == "All Students":
        filtered_data = data
    else:
        course_id = [k for k, v in course_mapping.items() if v == selected_course][0]
        filtered_data = data[data['Course'] == course_id]

    st.write(f"### 🎓 Demographic Distribution - {selected_course}")
    
    # List fitur demografi yang akan divisualisasikan
    demographic_features = [
        'Gender',
        'Daytime_evening_attendance',
        'Displaced',
        'Educational_special_needs',
        'Debtor',
        'Scholarship_holder',
        'International'
    ]

    # Buat layout 3 kolom
    rows = [demographic_features[i:i + 3] for i in range(0, len(demographic_features), 3)]

    # Loop per baris
    for row_features in rows:
        cols = st.columns(3)
        for idx, feature in enumerate(row_features):
            with cols[idx]:
                st.write(f"**{feature}**")
                
                # Buat DataFrame untuk Plotly
                plot_data = filtered_data.groupby([feature, 'Status']).size().reset_index(name='Count')
                
                # Visualisasi Plotly
                fig = px.bar(plot_data,
                             x=feature,
                             y='Count',
                             color='Status',
                             color_discrete_map={
                                 'Graduate': '#2ecc71',
                                 'Dropout': '#e74c3c',
                                 'Enrolled': '#3498db'
                             },
                             title=f"Distribusi Mahasiswa Berdasarkan {feature}",
                             labels={'Count': 'Jumlah Mahasiswa'},
                             text='Count',
                             barmode='stack')
                
                # Update layout untuk tampil lebih rapi
                fig.update_layout(height=400, margin=dict(l=0, r=0, t=40, b=0))
                fig.update_traces(texttemplate='%{text}', textposition='outside')
                
                # Render di Streamlit
                st.plotly_chart(fig, use_container_width=True)

        st.write("---")
    # --- Correlation Plot ---
    st.write("## 🔍 **Feature Correlation with Status**")
    
    # Pilihan tipe fitur
    correlation_type = st.radio("Pilih Jenis Fitur:", ["All Features", "Numerical Features", "Categorical Features"])

    # Merge fitur numerikal dan kategorikal jika 'All Features'
    if correlation_type == "All Features":
        selected_features = numerical_columns + categorical_columns
    elif correlation_type == "Numerical Features":
        selected_features = numerical_columns
    else:
        selected_features = categorical_columns

    # Map Status ke nilai numerik
    status_mapping = {'Graduate': 1, 'Dropout': 0, 'Enrolled': 2}
    data['Status_Num'] = data['Status'].map(status_mapping)

    # Fungsi untuk plot korelasi
    def plot_feature_correlations(df, target):
        corr = df[selected_features + [target]].corr(numeric_only=True)[target].drop(target).sort_values()
        corr_df = pd.DataFrame({
            'Feature': corr.index,
            'Correlation': corr.values
        }).reset_index(drop=True)
        
        # Visualisasi menggunakan Plotly
        fig = px.bar(corr_df, x='Feature', y='Correlation',
                     color='Correlation', color_continuous_scale='RdBu',
                     title=f'Correlation of Features with {target}',
                     labels={'Correlation': 'Pearson Correlation'})
        
        fig.update_layout(height=600, xaxis_title="Features", yaxis_title="Correlation",
                          xaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig, use_container_width=True)

    # Plot hasil korelasi
    plot_feature_correlations(data, 'Status_Num')

    # Hapus kolom numerik sementara
    data.drop(columns=['Status_Num'], inplace=True)
    st.write("---")

    # Judul
    st.write(f"## 📊 Status Distribution - {selected_course}")

    # Group by Status dan hitung jumlah
    status_counts = filtered_data['Status'].value_counts().reset_index()
    status_counts.columns = ['Status', 'Count']

    # Plotly Pie Chart
    fig = px.pie(status_counts, 
                values='Count', 
                names='Status', 
                color='Status',
                color_discrete_map={
                    'Graduate': '#2ecc71',
                    'Dropout': '#e74c3c',
                    'Enrolled': '#3498db'
                },
                title=f'Proportion of Student Status in {selected_course}')

    # Update layout
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(height=500, margin=dict(l=0, r=0, t=40, b=0))

    # Render Plotly di Streamlit
    st.plotly_chart(fig, use_container_width=True)


# =======================
# 🔍 Prediction Page
# =======================
if menu == "🔍 Prediction Page":
    st.title("🔍 Prediction Page - Student Dropout Prediction")
    
    # Load Model (pastikan model sudah disimpan dengan nama 'dropout_model.pkl')
    import joblib
    model = joblib.load('dropout_model.pkl')

    # ===================
    # 1️⃣ Input Features
    # ===================
    st.write("### 🎓 Student Information Form")
    course_mapping ={
        33: 'Biofuel Production Technologies',
        171: 'Animation and Multimedia Design',
        8014: 'Social Service (evening attendance)',
        9003: 'Agronomy',
        9070: 'Communication Design',
        9085: 'Veterinary Nursing',
        9119: 'Informatics Engineering',
        9130: 'Equinculture',
        9147: 'Management',
        9238: 'Social Service',
        9254: 'Tourism',
        9500: 'Nursing',
        9556: 'Oral Hygiene',
        9670: 'Advertising and Marketing Management',
        9773: 'Journalism and Communication',
        9853: 'Basic Education',
        9991: 'Management (evening attendance)'
    }
    fatheroc_mapping = {
        0: 'Student',
        1: 'Representatives of the Legislative Power and Executive Bodies, Directors, Directors and Executive Managers',
        2: 'Specialists in Intellectual and Scientific Activities',
        3: 'Intermediate Level Technicians and Professions',
        4: 'Administrative staff',
        5: 'Personal Services, Security and Safety Workers and Sellers',
        6: 'Farmers and Skilled Workers in Agriculture, Fisheries and Forestry',
        7: 'Skilled Workers in Industry, Construction and Craftsmen',
        8: 'Installation and Machine Operators and Assembly Workers',
        9: 'Unskilled Workers',
        10: 'Armed Forces Professions',
        90: 'Other Situation',
        99: '(blank)',
        101: 'Armed Forces Officers',
        102: 'Armed Forces Sergeants',
        103: 'Other Armed Forces personnel',
        112: 'Directors of administrative and commercial services',
        114: 'Hotel, catering, trade and other services directors',
        121: 'Specialists in the physical sciences, mathematics, engineering and related techniques',
        122: 'Health professionals',
        123: 'Teachers',
        124: 'Specialists in finance, accounting, administrative organization, public and commercial relations',
        131: 'Intermediate level science and engineering technicians and professions',
        132: 'Technicians and professionals, of intermediate level of health',
        134: 'Intermediate level technicians from legal, social, sports, cultural and similar services',
        135: 'Information and communication technology technicians',
        141: 'Office workers, secretaries in general and data processing operators',
        143: 'Data, accounting, statistical, financial services and registry-related operators',
        144: 'Other administrative support staff',
        151: 'Personal service workers',
        152: 'Sellers',
        153: 'Personal care workers and the like',
        154: 'Protection and security services personnel',
        161: 'Market-oriented farmers and skilled agricultural and animal production workers',
        163: 'Farmers, livestock keepers, fishermen, hunters and gatherers, subsistence',
        171: 'Skilled construction workers and the like, except electricians',
        172: 'Skilled workers in metallurgy, metalworking and similar',
        174: 'Skilled workers in electricity and electronics',
        175: 'Workers in food processing, woodworking, clothing and other industries and crafts',
        181: 'Fixed plant and machine operators',
        182: 'Assembly workers',
        183: 'Vehicle drivers and mobile equipment operators',
        192: 'Unskilled workers in agriculture, animal production, fisheries and forestry',
        193: 'Unskilled workers in extractive industry, construction, manufacturing and transport',
        194: 'Meal preparation assistants',
        195: 'Street vendors (except food) and street service providers'
    }
    # Sidebar untuk input data
    with st.form(key='student_form'):
        # Form Input Sesuai dengan Selected Features
        course = st.selectbox("Course", list(course_mapping.values()))
        previous_grade = st.number_input("Previous Qualification Grade", 0.0, 1000.0, 10.0, 0.1)
        admission_grade = st.number_input("Admission Grade", 0.0, 1000.0, 10.0, 0.1)
        tuition_up_to_date = st.selectbox("Tuition Fees Up-to-date", ["Yes", "No"])
        age = st.number_input("Age at Enrollment", min_value=15, max_value=60, value=20)
        scholarship_holder = st.selectbox("Scholarship Holder", ["Yes", "No"])
        first_sem_grade = st.number_input("1st Semester Grade", 0.0, 1000.0, 10.0, 0.1)
        second_sem_grade = st.number_input("2nd Semester Grade", 0.0, 1000.0, 10.0, 0.1)
        first_sem_eval = st.number_input("1st Semester Evaluations", min_value=0, max_value=60, value=0)
        second_sem_eval = st.number_input("2nd Semester Evaluations", min_value=0, max_value=60, value=0)
        second_sem_approved = st.number_input("2nd Semester Approved Units", min_value=0, max_value=60, value=0)
        father_occupation = st.selectbox("Father's Occupation", list(fatheroc_mapping.values()))

        # Tombol Submit
        submit_button = st.form_submit_button(label="Predict Status")
    
    # ==========================
    # 2️⃣ Feature Engineering
    # ==========================
    if submit_button:
        # Mapping input ke format model
        tuition_map = {'Yes': 1, 'No': 0}
        scholarship_map = {'Yes': 1, 'No': 0}
        
        # Dapatkan kode Course
        course_id = [k for k, v in course_mapping.items() if v == course][0]
        # Mendapatkan ID dari mapping
        fatheroc_id = [k for k, v in fatheroc_mapping.items() if v == father_occupation][0]
        
        # Buat DataFrame dari input user
        input_data = pd.DataFrame({
            'Course': [course_id],
            'Previous_qualification_grade': [previous_grade],
            'Admission_grade': [admission_grade],
            'Tuition_fees_up_to_date': [tuition_map[tuition_up_to_date]],
            'Age_at_enrollment': [age],
            'Scholarship_holder': [scholarship_map[scholarship_holder]],
            'Curricular_units_1st_sem_grade': [first_sem_grade],
            'Curricular_units_2nd_sem_grade': [second_sem_grade],
            'Curricular_units_1st_sem_evaluations': [first_sem_eval],
            'Curricular_units_2nd_sem_evaluations': [second_sem_eval],
            'Curricular_units_2nd_sem_approved': [second_sem_approved],
            'Fathers_occupation': [fatheroc_id]
        })
        
        # ==========================
        # 3️⃣ Prediction Process
        # ==========================
        prediction = model.predict(input_data)
        prediction_proba = model.predict_proba(input_data)

        # Mapping hasil prediksi
        status_mapping = {0: 'Dropout', 1: 'Graduate'}
        predicted_status = status_mapping[prediction[0]]
        
        # ==========================
        # 4️⃣ Visualisasi Hasil
        # ==========================
        st.write("### 🎯 **Prediction Result**")
        
        # Warna berdasarkan hasil prediksi
        color_map = {'Dropout': '#e74c3c', 'Graduate': '#2ecc71'}
        
        # Visualisasi
        fig = px.pie(names=['Graduate', 'Dropout'],
                     values=[prediction_proba[0][1], prediction_proba[0][0]],
                     color=['Graduate', 'Dropout'],
                     color_discrete_map=color_map,
                     title="Probability Distribution")
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
        
        # Display hasil prediksi
        st.success(f"The student is predicted to **{predicted_status}**.")

        # Detail probabilitas
        st.write(f"**Confidence Level:**")
        st.write(f"- Graduate: {prediction_proba[0][1] * 100:.2f}%")
        st.write(f"- Dropout: {prediction_proba[0][0] * 100:.2f}%")

