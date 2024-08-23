
import shap

def explain_model(model, data):
    explainer = shap.Explainer(model)
    shap_values = explainer(data)
    return shap_values
