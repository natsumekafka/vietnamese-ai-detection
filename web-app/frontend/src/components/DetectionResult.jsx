import React from 'react';
import { CheckCircle, AlertTriangle } from 'lucide-react';

export default function DetectionResult({ result }) {
  if (!result) return null;

  const { is_human, human_prob, ai_prob, message } = result;
  
  // Decide the dominant score and styles
  const dominantProb = is_human ? human_prob : ai_prob;
  const isSafe = is_human;
  
  const progressBarColor = isSafe ? 'bg-green-500' : 'bg-red-500';
  const bgColor = isSafe ? 'bg-green-50' : 'bg-red-50';
  const textColor = isSafe ? 'text-green-700' : 'text-red-700';
  const borderColor = isSafe ? 'border-green-200' : 'border-red-200';
  
  return (
    <div className={`h-full flex flex-col justify-center p-6 rounded-2xl border ${borderColor} ${bgColor} transition-all duration-500 ease-in-out`}>
      <div className="flex items-center gap-3 mb-4">
        {isSafe ? (
          <CheckCircle className="w-8 h-8 text-green-600" />
        ) : (
          <AlertTriangle className="w-8 h-8 text-red-600" />
        )}
        <h3 className={`text-2xl font-bold ${textColor}`}>
          {isSafe ? 'Khả năng cao do Người viết' : 'Khả năng cao do AI tạo ra'}
        </h3>
      </div>
      
      <div className="mb-2 flex justify-between text-sm font-medium text-gray-700">
        <span>Độ tin cậy (Confidence Score)</span>
        <span className={textColor}>{dominantProb.toFixed(1)}%</span>
      </div>
      
      {/* Progress Bar Container */}
      <div className="w-full bg-gray-200 rounded-full h-4 mb-4 overflow-hidden shadow-inner">
        <div 
          className={`h-4 rounded-full ${progressBarColor} transition-all duration-1000 ease-out relative`} 
          style={{ width: `${dominantProb}%` }}
        >
          {/* Subtle shine effect */}
          <div className="absolute top-0 left-0 right-0 bottom-0 bg-gradient-to-b from-white/30 to-transparent"></div>
        </div>
      </div>
      
      <div className="flex justify-between text-xs text-gray-500 mt-2">
        <div className="flex flex-col items-center">
          <span className="font-semibold text-green-600">Human</span>
          <span>{human_prob.toFixed(1)}%</span>
        </div>
        <div className="flex flex-col items-center">
          <span className="font-semibold text-red-600">AI</span>
          <span>{ai_prob.toFixed(1)}%</span>
        </div>
      </div>
    </div>
  );
}
