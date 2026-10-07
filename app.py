import streamlit as st
import joblib
import pandas as pd
from datetime import date


# ============================================================
# LOAD TRAINED MODEL AND PREPROCESSOR
# ============================================================

model = joblib.load("random_forest_model.pkl")
preprocessor = joblib.load("preprocessor.pkl")


# ============================================================
# PAGE TITLE
# ============================================================

st.title("PredictSecBugs")
st.subheader("Security Bug Prediction")
st.write(
    "PredictSecBugs is a Machine Learning-based application that predicts "
    "whether a software commit may contain a security bug using various "
    "code metrics. The application uses a Random Forest Classifier trained "
    "on software commit data."
)

st.info(
    "Machine Learning Model: Random Forest Classifier\n\n"
    "Test Accuracy: 95.45%"
)

st.write(
    "Enter the code metrics below to predict whether a commit is buggy."
)

st.subheader("How It Works")

st.write(
    "1. Enter the commit and code metrics.\n"
    "2. The data is processed using the trained preprocessor.\n"
    "3. The Random Forest model analyzes the metrics.\n"
    "4. The application predicts BUGGY or NOT BUGGY."
)

# ============================================================
# INPUT FIELDS
# ============================================================

commit_date = st.date_input(
    "Commit Date",
    date.today(),
    min_value=date(2000, 1, 1),
    max_value=date.today()
)

extension = st.selectbox(
    "File Extension",
    [".py", ".java", ".c", ".cpp", ".h", ".hpp", ".js", ".ts",".php"]
)

ecosystem = st.selectbox(
    "Ecosystem",
    ["PyPI", "Maven", "NuGet", "NPM", "OSS-Fuzz", "GHSA","Other"]
)

avg_line_code = st.number_input(
    "Average Line Code",
    min_value=0.0
)

count_decl_class = st.number_input(
    "Count Declaration Class",
    min_value=0.0
)

ratio_comment_to_code = st.number_input(
    "Ratio Comment To Code",
    min_value=0.0
)

count_stmt_exe = st.number_input(
    "Count Statement Executable",
    min_value=0.0
)

avg_cyclomatic_strict = st.number_input(
    "Average Cyclomatic Strict",
    min_value=0.0
)

count_line = st.number_input(
    "Count Line",
    min_value=0.0
)

sum_cyclomatic = st.number_input(
    "Sum Cyclomatic",
    min_value=0.0
)

avg_cyclomatic = st.number_input(
    "Average Cyclomatic",
    min_value=0.0
)

sum_essential = st.number_input(
    "Sum Essential",
    min_value=0.0
)

max_cyclomatic = st.number_input(
    "Maximum Cyclomatic",
    min_value=0.0
)

avg_line_comment = st.number_input(
    "Average Line Comment",
    min_value=0.0
)

avg_cyclomatic_modified = st.number_input(
    "Average Cyclomatic Modified",
    min_value=0.0
)

avg_essential = st.number_input(
    "Average Essential",
    min_value=0.0
)

sum_cyclomatic_modified = st.number_input(
    "Sum Cyclomatic Modified",
    min_value=0.0
)

count_line_comment = st.number_input(
    "Count Line Comment",
    min_value=0.0
)

count_line_code = st.number_input(
    "Count Line Code",
    min_value=0.0
)

max_cyclomatic_modified = st.number_input(
    "Maximum Cyclomatic Modified",
    min_value=0.0
)

count_line_blank = st.number_input(
    "Count Line Blank",
    min_value=0.0
)

count_stmt_decl = st.number_input(
    "Count Statement Declaration",
    min_value=0.0
)

avg_line = st.number_input(
    "Average Line",
    min_value=0.0
)

max_essential = st.number_input(
    "Maximum Essential",
    min_value=0.0
)

count_decl_function = st.number_input(
    "Count Declaration Function",
    min_value=0.0
)

max_nesting = st.number_input(
    "Maximum Nesting",
    min_value=0.0
)

avg_line_blank = st.number_input(
    "Average Line Blank",
    min_value=0.0
)

sum_cyclomatic_strict = st.number_input(
    "Sum Cyclomatic Strict",
    min_value=0.0
)

count_stmt = st.number_input(
    "Count Statement",
    min_value=0.0
)


# ============================================================
# PREDICTION
# ============================================================

if st.button("Predict"):

    # --------------------------------------------------------
    # CREATE INPUT DATAFRAME
    # --------------------------------------------------------

    input_data = pd.DataFrame([{

        "commit_date": pd.Timestamp(commit_date).timestamp(),

        "extension": extension,

        "AvgLineCode": avg_line_code,

        "CountDeclClass": count_decl_class,

        "RatioCommentToCode": ratio_comment_to_code,

        "CountStmtExe": count_stmt_exe,

        "AvgCyclomaticStrict": avg_cyclomatic_strict,

        "CountLine": count_line,

        "SumCyclomatic": sum_cyclomatic,

        "AvgCyclomatic": avg_cyclomatic,

        "SumEssential": sum_essential,

        "MaxCyclomatic": max_cyclomatic,

        "AvgLineComment": avg_line_comment,

        "AvgCyclomaticModified": avg_cyclomatic_modified,

        "AvgEssential": avg_essential,

        "SumCyclomaticModified": sum_cyclomatic_modified,

        "CountLineComment": count_line_comment,

        "CountLineCode": count_line_code,

        "MaxCyclomaticModified": max_cyclomatic_modified,

        "CountLineBlank": count_line_blank,

        "CountStmtDecl": count_stmt_decl,

        "AvgLine": avg_line,

        "MaxEssential": max_essential,

        "CountDeclFunction": count_decl_function,

        "MaxNesting": max_nesting,

        "AvgLineBlank": avg_line_blank,

        "SumCyclomaticStrict": sum_cyclomatic_strict,

        "CountStmt": count_stmt,

        "Ecosystem": ecosystem

    }])


    # --------------------------------------------------------
    # PREPROCESS INPUT
    # --------------------------------------------------------

    input_processed = preprocessor.transform(input_data)


    # --------------------------------------------------------
    # MAKE PREDICTION
    # --------------------------------------------------------

    prediction = model.predict(input_processed)[0]


    # --------------------------------------------------------
    # GET BUG PROBABILITY
    # --------------------------------------------------------

    probability = model.predict_proba(input_processed)[0][1]


    # --------------------------------------------------------
    # DISPLAY RESULT
    # --------------------------------------------------------

    st.subheader("Prediction Result")
    st.write(
    "The model predicts whether the given code metrics indicate a "
    "potentially buggy commit."
)


    if prediction == 1:
     st.error("Prediction: BUGGY")
     st.write(
        "The model identifies this commit as potentially containing "
        "a security-related bug."
    )
    else:
     st.success("Prediction: NOT BUGGY")
     st.write(
        "The model does not identify this commit as potentially buggy "
        "based on the provided code metrics."
    )

    # Display probability

    st.write(
        f"Bug Probability: {probability * 100:.2f}%"
    )
    st.subheader("Important Features")

st.write(
    "The Random Forest model identified these code metrics as "
    "important for its predictions."
)

feature_importance_data = {
    "Feature": [
        "CountDeclClass",
        "AvgLineBlank",
        "AvgLineComment",
        "MaxNesting",
        "CountDeclFunction",
        "AvgLineCode",
        "AvgCyclomaticModified",
        "AvgCyclomaticStrict",
        "MaxCyclomatic",
        "AvgEssential"
    ],
    "Importance": [
        0.294904,
        0.141384,
        0.132300,
        0.055567,
        0.033645,
        0.027869,
        0.021797,
        0.019421,
        0.018697,
        0.018661
    ]
}

feature_df = pd.DataFrame(feature_importance_data)

st.bar_chart(
    feature_df.set_index("Feature")
)
st.subheader("Why did the model make this prediction?")

st.write(
    "The Random Forest model uses different code metrics when making "
    "its prediction. The following features were the most important "
    "during model training:"
)

top_features = feature_df.head(5)

for _, row in top_features.iterrows():
    st.write(
        f"• {row['Feature']} — Importance: {row['Importance']:.3f}"
    )
st.subheader("Project Information")

st.write("Model: Random Forest Classifier")
st.write("Dataset: PredictSecBugs software commit dataset")
st.write("Purpose: Predict potentially buggy software commits using code metrics.")
st.write("Test Accuracy: 95.45%")
