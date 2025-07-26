import React, { useState } from 'react';
import { Brain, Zap, Activity, Play } from 'lucide-react';

function NeuralNetworkForm() {
  // Model training state
  const [modelForm, setModelForm] = useState({
    hiddenLayerSize: '',
    activation: 'relu',
    algorithm: 'adam',
    alpha: '',
    maxIterations: ''
  });

  // Prediction state
  const [predictionInputs, setPredictionInputs] = useState([
    { name: "age", value: "", label: "Edad", type: "number" },
    { 
      name: "gender", 
      value: "", 
      label: "Género", 
      type: "select",
      options: ["Masculino", "Femenino", "Otro"] 
    },
    { 
      name: "education", 
      value: "", 
      label: "Educación", 
      type: "select",
      options: ["Primaria", "Secundaria", "Universidad", "Postgrado"] 
    },
    { name: "country", value: "", label: "País", type: "text" },
    { name: "ethnicity", value: "", label: "Etnia", type: "text" },
    { name: "nscore", value: "", label: "Puntuación N", type: "number" },
    { name: "escore", value: "", label: "Puntuación E", type: "number" },
    { name: "oscore", value: "", label: "Puntuación O", type: "number" },
    { name: "ascore", value: "", label: "Puntuación A", type: "number" },
    { name: "cscore", value: "", label: "Puntuación C", type: "number" },
    { name: "impulsive", value: "", label: "Impulsividad", type: "number" },
    { name: "ss", value: "", label: "Búsqueda de sensaciones", type: "number" },
  ]);

  const [isProcessing, setIsProcessing] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    setIsProcessing(true);
    
    // Combine all form data
    const formData = {
      model: modelForm,
      prediction: predictionInputs.reduce((acc, input) => {
        acc[input.name] = input.value;
        return acc;
      }, {})
    };

    // Simulate API call
    console.log('Enviando datos al backend:', formData);
    setTimeout(() => {
      setIsProcessing(false);
      alert('Proceso completado con éxito');
    }, 3000);
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      {/* Training Section */}
      <div className="bg-white rounded-2xl shadow-xl border border-gray-300 p-8 hover:shadow-2xl transition-all duration-300">
        <div className="flex items-center space-x-3 mb-8">
          <div className="p-3 bg-black rounded-xl">
            <Brain className="h-6 w-6 text-white" />
          </div>
          <div>
            <h2 className="text-2xl font-semibold text-gray-900">Configuración del Modelo</h2>
            <p className="text-gray-600">Define los parámetros para entrenar tu modelo</p>
          </div>
        </div>

        <div className="space-y-8">

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label htmlFor="hiddenLayerSize" className="block text-sm font-medium text-gray-700 mb-3">
                Tamaño de Capas Ocultas
              </label>
              <input
                type="number"
                id="hiddenLayerSize"
                value={modelForm.hiddenLayerSize}
                onChange={(e) => setModelForm({ ...modelForm, hiddenLayerSize: e.target.value })}
                className="w-full px-4 py-4 border border-gray-300 rounded-xl focus:ring-2 focus:ring-black focus:border-transparent transition-all duration-200 bg-white text-lg"
                placeholder="128"
                min="1"
                required
              />
            </div>

            <div>
              <label htmlFor="alpha" className="block text-sm font-medium text-gray-700 mb-3">
                Alpha
              </label>
              <input
                type="number"
                id="alpha"
                value={modelForm.alpha}
                onChange={(e) => setModelForm({ ...modelForm, alpha: e.target.value })}
                className="w-full px-4 py-4 border border-gray-300 rounded-xl focus:ring-2 focus:ring-black focus:border-transparent transition-all duration-200 bg-white text-lg"
                placeholder="0.001"
                step="0.0001"
                min="0"
                max="1"
                required
              />
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label htmlFor="activation" className="block text-sm font-medium text-gray-700 mb-3">
                Activación
              </label>
              <select
                id="activation"
                value={modelForm.activation}
                onChange={(e) => setModelForm({ ...modelForm, activation: e.target.value })}
                className="w-full px-4 py-4 border border-gray-300 rounded-xl focus:ring-2 focus:ring-black focus:border-transparent transition-all duration-200 bg-white text-lg"
              >
                <option value="relu">ReLU</option>
                <option value="sigmoid">Sigmoid</option>
                <option value="tanh">Tanh</option>
                <option value="softmax">Softmax</option>
                <option value="linear">Linear</option>
              </select>
            </div>

            <div>
              <label htmlFor="algorithm" className="block text-sm font-medium text-gray-700 mb-3">
                Algoritmo
              </label>
              <select
                id="algorithm"
                value={modelForm.algorithm}
                onChange={(e) => setModelForm({ ...modelForm, algorithm: e.target.value })}
                className="w-full px-4 py-4 border border-gray-300 rounded-xl focus:ring-2 focus:ring-black focus:border-transparent transition-all duration-200 bg-white text-lg"
              >
                <option value="adam">Adam</option>
                <option value="sgd">SGD</option>
                <option value="rmsprop">RMSprop</option>
                <option value="adagrad">Adagrad</option>
                <option value="adadelta">Adadelta</option>
              </select>
            </div>
          </div>

          <div>
            <label htmlFor="maxIterations" className="block text-sm font-medium text-gray-700 mb-3">
              Iteraciones Máximas
            </label>
            <input
              type="number"
              id="maxIterations"
              value={modelForm.maxIterations}
              onChange={(e) => setModelForm({ ...modelForm, maxIterations: e.target.value })}
              className="w-full px-4 py-4 border border-gray-300 rounded-xl focus:ring-2 focus:ring-black focus:border-transparent transition-all duration-200 bg-white text-lg"
              placeholder="1000"
              min="1"
              required
            />
          </div>
        </div>
      </div>

      {/* Prediction Section */}
      <div className="bg-white rounded-2xl shadow-xl border border-gray-300 p-8 hover:shadow-2xl transition-all duration-300">
        <div className="flex items-center space-x-3 mb-8">
          <div className="p-3 bg-black rounded-xl">
            <Zap className="h-6 w-6 text-white" />
          </div>
          <div>
            <h2 className="text-2xl font-semibold text-gray-900">Datos para Predicción</h2>
            <p className="text-gray-600">Ingrese los valores para realizar la predicción</p>
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-4">
            Variables de Entrada
          </label>
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4">
            {predictionInputs.map((input, index) => (
              <div key={index}>
                <label htmlFor={`input-${input.name}`} className="block text-xs font-medium text-gray-600 mb-2">
                  {input.label}
                </label>
                
                {input.type === "select" ? (
                  <select
                    id={`input-${input.name}`}
                    value={input.value}
                    onChange={(e) => {
                      const newInputs = [...predictionInputs];
                      newInputs[index] = { ...newInputs[index], value: e.target.value };
                      setPredictionInputs(newInputs);
                    }}
                    className="w-full px-3 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent transition-all duration-200 bg-white"
                    required
                  >
                    <option value="">Seleccione...</option>
                    {input.options.map((option, i) => (
                      <option key={i} value={option}>
                        {option}
                      </option>
                    ))}
                  </select>
                ) : (
                  <input
                    type={input.type}
                    id={`input-${input.name}`}
                    value={input.value}
                    onChange={(e) => {
                      const newInputs = [...predictionInputs];
                      newInputs[index] = { ...newInputs[index], value: e.target.value };
                      setPredictionInputs(newInputs);
                    }}
                    className="w-full px-3 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent transition-all duration-200 bg-white"
                    placeholder={input.type === "number" ? "0.0" : ""}
                    step={input.type === "number" ? "any" : undefined}
                    required
                  />
                )}
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Submit Button Card */}
      <div className="bg-white rounded-2xl shadow-xl border border-gray-300 p-8 hover:shadow-2xl transition-all duration-300">
        <button
          type="button"
          onClick={handleSubmit}
          disabled={isProcessing}
          className="w-full bg-black text-white py-5 px-8 rounded-xl font-semibold text-xl hover:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 transition-all duration-200 flex items-center justify-center space-x-3 disabled:opacity-70 disabled:cursor-not-allowed shadow-lg hover:shadow-xl"
        >
          {isProcessing ? (
            <>
              <Activity className="h-6 w-6 animate-pulse" />
              <span>Procesando...</span>
            </>
          ) : (
            <>
              <Play className="h-6 w-6" />
              <span>Iniciar Proceso</span>
            </>
          )}
        </button>
      </div>
    </div>
  );
}

export default NeuralNetworkForm;