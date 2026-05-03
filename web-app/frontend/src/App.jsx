import React, { useState } from 'react';
import { ShieldCheck, Loader2 } from 'lucide-react';
import DetectionResult from './components/DetectionResult';

const API_URL = 'http://localhost:8000/v1/detect';

function App() {
  const [text, setText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const wordCount = text.trim() === '' ? 0 : text.trim().split(/\s+/).length;

  const handleTextChange = (e) => {
    setText(e.target.value);
    if (error) setError('');
  };

  const handleAnalyze = async () => {
    if (wordCount < 100) {
      setError(`Văn bản quá ngắn. Vui lòng nhập ít nhất 100 chữ (hiện tại: ${wordCount} chữ) để hệ thống AI có đủ dữ liệu phân tích văn phong.`);
      return;
    }
    if (wordCount > 2000) {
      setError(`Văn bản quá dài. Vui lòng nhập tối đa 2000 chữ (hiện tại: ${wordCount} chữ) để tránh quá tải hệ thống.`);
      return;
    }

    setIsLoading(true);
    setError('');
    setResult(null);

    try {
      const response = await fetch(API_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ content: text.trim() }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Có lỗi xảy ra khi phân tích.');
      }

      setResult(data);
    } catch (err) {
      setError(err.message || 'Không thể kết nối đến máy chủ. Vui lòng kiểm tra xem backend đã chạy chưa.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="w-full max-w-6xl mx-auto p-4 md:p-8">
      <div className="glassmorphism rounded-3xl p-8 shadow-2xl relative overflow-hidden">
        {/* Background decorations */}
        <div className="absolute top-[-10%] right-[-5%] w-64 h-64 bg-blue-400 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob"></div>
        <div className="absolute bottom-[-10%] left-[-5%] w-72 h-72 bg-purple-400 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-2000"></div>

        <div className="relative z-10">
          <div className="text-center mb-8">
            <div className="flex justify-center mb-4">
              <div className="bg-indigo-100 p-4 rounded-full">
                <ShieldCheck className="w-12 h-12 text-indigo-600" />
              </div>
            </div>
            <h1 className="text-4xl font-extrabold text-gray-900 tracking-tight mb-2">
              Phát Hiện Văn Bản AI
            </h1>
            <p className="text-gray-500 text-lg max-w-2xl mx-auto">
              Sử dụng mô hình PhoBERT v2 để phân tích và kiểm tra xem văn bản tiếng Việt của bạn được viết bởi người hay trí tuệ nhân tạo.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {/* Cột trái: Nhập văn bản */}
            <div className="space-y-4 flex flex-col">
              <div className="relative flex-1">
                <textarea
                  value={text}
                  onChange={handleTextChange}
                  placeholder="Nhập hoặc dán đoạn văn bản cần phân tích vào đây..."
                  className="w-full h-full min-h-[300px] p-5 text-gray-700 bg-white border border-gray-200 rounded-2xl shadow-sm focus:ring-4 focus:ring-indigo-100 focus:border-indigo-500 resize-none transition-all duration-200 text-lg"
                />
                <div className="absolute bottom-4 right-4 text-sm font-medium text-gray-400 bg-white/80 px-2 py-1 rounded shadow-sm">
                  {wordCount} chữ | {text.length} ký tự
                </div>
              </div>

              {error && (
                <div className="p-4 bg-red-50 text-red-600 rounded-xl text-sm font-medium border border-red-100">
                  {error}
                </div>
              )}

              <button
                onClick={handleAnalyze}
                disabled={isLoading || text.length === 0}
                className={`w-full py-4 rounded-xl text-white font-bold text-lg shadow-lg transition-all duration-300 flex justify-center items-center gap-2 mt-auto
                  ${isLoading || text.length === 0
                    ? 'bg-gray-400 cursor-not-allowed'
                    : 'bg-indigo-600 hover:bg-indigo-700 hover:shadow-indigo-200 hover:-translate-y-1'
                  }
                `}
              >
                {isLoading ? (
                  <>
                    <Loader2 className="w-6 h-6 animate-spin" />
                    Đang phân tích...
                  </>
                ) : (
                  'Phân tích văn bản'
                )}
              </button>
            </div>

            {/* Cột phải: Kết quả */}
            <div className="flex flex-col h-full min-h-[300px]">
              {result ? (
                <DetectionResult result={result} />
              ) : (
                <div className="flex-1 flex flex-col items-center justify-center p-8 border-2 border-dashed border-gray-300 rounded-2xl bg-gray-50/50 text-gray-400 transition-all duration-300 hover:bg-gray-50">
                  <ShieldCheck className="w-20 h-20 mb-4 opacity-20" />
                  <p className="text-center font-medium text-lg">Kết quả phân tích sẽ hiển thị tại đây</p>
                  <p className="text-center text-sm mt-2 opacity-60">Nhập văn bản vào ô bên trái và bấm phân tích</p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      <div className="text-center mt-8 text-sm text-gray-500">
        <p>Hệ thống hỗ trợ bởi PhoBERT v2 (vinai/phobert-base-v2)</p>
      </div>
    </div>
  );
}

export default App;
