{% set models_to_generate = codegen.get_models(directory='staging', prefix='') %}
{{ codegen.generate_model_yaml(
    model_names = models_to_generate
) }}