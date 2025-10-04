'use client';
import { useState, useEffect } from 'react';

export default function Home() {
  const [currentSlide, setCurrentSlide] = useState(0);
  
  const slides = [
    {
      title: "Охотничьи ножи",
      description: "Профессиональные ножи из высококачественной стали",
      price: "от 2 500 ₽",
      image: "🗡️"
    },
    {
      title: "Туристические топоры",
      description: "Надёжные инструменты для походов и выживания",
      price: "от 3 800 ₽",
      image: "🪓"
    },
    {
      title: "Складные ножи",
      description: "Компактные и удобные для повседневного ношения",
      price: "от 1 900 ₽",
      image: "🔪"
    }
  ];

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentSlide((prev) => (prev + 1) % slides.length);
    }, 5000);
    return () => clearInterval(timer);
  }, []);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-primary text-white shadow-lg">
        <div className="container mx-auto px-4 py-4">
          <div className="flex justify-between items-center">
            <div className="flex items-center space-x-2">
              <span className="text-3xl">🔪</span>
              <h1 className="text-2xl font-bold">Knife Store</h1>
            </div>
            <nav className="hidden md:flex space-x-6">
              <a href="#catalog" className="hover:text-accent transition">Каталог</a>
              <a href="#new" className="hover:text-accent transition">Новинки</a>
              <a href="#about" className="hover:text-accent transition">О нас</a>
              <a href="#contacts" className="hover:text-accent transition">Контакты</a>
            </nav>
            <button className="bg-accent px-6 py-2 rounded-lg hover:bg-red-600 transition">
              🛒 Корзина
            </button>
          </div>
        </div>
      </header>

      {/* Hero Slider */}
      <section className="relative h-[600px] bg-gradient-to-br from-gray-800 to-gray-900 overflow-hidden">
        {slides.map((slide, index) => (
          <div
            key={index}
            className={`absolute inset-0 transition-opacity duration-1000 ${
              index === currentSlide ? 'opacity-100' : 'opacity-0'
            }`}
          >
            <div className="container mx-auto px-4 h-full flex items-center">
              <div className="grid md:grid-cols-2 gap-8 items-center w-full">
                <div className="text-white space-y-6">
                  <h2 className="text-5xl md:text-6xl font-bold">{slide.title}</h2>
                  <p className="text-xl text-gray-300">{slide.description}</p>
                  <div className="flex items-center space-x-4">
                    <span className="text-3xl font-bold text-accent">{slide.price}</span>
                    <button className="bg-accent px-8 py-3 rounded-lg text-lg font-semibold hover:bg-red-600 transition">
                      Смотреть товары
                    </button>
                  </div>
                </div>
                <div className="text-center">
                  <span className="text-[200px] md:text-[300px] opacity-20">{slide.image}</span>
                </div>
              </div>
            </div>
          </div>
        ))}
        
        {/* Indicators */}
        <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 flex space-x-3">
          {slides.map((_, index) => (
            <button
              key={index}
              onClick={() => setCurrentSlide(index)}
              className={`h-1 transition-all ${
                index === currentSlide ? 'w-12 bg-accent' : 'w-8 bg-white/50'
              }`}
            />
          ))}
        </div>
      </section>

      {/* Новинки */}
      <section id="new" className="py-16 bg-white">
        <div className="container mx-auto px-4">
          <h2 className="text-4xl font-bold text-center mb-12 text-primary">
            🔥 Новинки
          </h2>
          <div className="grid md:grid-cols-3 gap-8">
            {[
              { name: "Нож Bear", price: "3 500 ₽", badge: "Хит" },
              { name: "Топор Viking", price: "4 200 ₽", badge: "New" },
              { name: "Нож Tactical", price: "2 900 ₽", badge: "Sale" }
            ].map((product, i) => (
              <div key={i} className="bg-gray-50 rounded-xl p-6 hover:shadow-xl transition group">
                <div className="relative">
                  <div className="text-8xl text-center mb-4 group-hover:scale-110 transition">
                    {i === 1 ? '🪓' : '🗡️'}
                  </div>
                  <span className="absolute top-0 right-0 bg-accent text-white px-3 py-1 rounded-full text-sm">
                    {product.badge}
                  </span>
                </div>
                <h3 className="text-xl font-bold text-primary mb-2">{product.name}</h3>
                <p className="text-gray-600 mb-4">Сталь 95Х18, рукоять орех</p>
                <div className="flex justify-between items-center">
                  <span className="text-2xl font-bold text-accent">{product.price}</span>
                  <button className="bg-primary text-white px-4 py-2 rounded-lg hover:bg-gray-800 transition">
                    В корзину
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Популярные категории */}
      <section className="py-16 bg-gray-100">
        <div className="container mx-auto px-4">
          <h2 className="text-4xl font-bold text-center mb-12 text-primary">
            📂 Популярные категории
          </h2>
          <div className="grid md:grid-cols-4 gap-6">
            {[
              { icon: "🗡️", name: "Охотничьи ножи", count: 45 },
              { icon: "🪓", name: "Топоры", count: 23 },
              { icon: "🔪", name: "Складные ножи", count: 67 },
              { icon: "⚔️", name: "Коллекционные", count: 12 }
            ].map((cat, i) => (
              <div key={i} className="bg-white rounded-xl p-6 text-center hover:shadow-lg transition cursor-pointer group">
                <div className="text-6xl mb-4 group-hover:scale-125 transition">{cat.icon}</div>
                <h3 className="text-lg font-bold text-primary mb-2">{cat.name}</h3>
                <p className="text-gray-500">{cat.count} товаров</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Преимущества */}
      <section className="py-16 bg-primary text-white">
        <div className="container mx-auto px-4">
          <div className="grid md:grid-cols-3 gap-8 text-center">
            <div>
              <div className="text-5xl mb-4">🚚</div>
              <h3 className="text-xl font-bold mb-2">Бесплатная доставка</h3>
              <p className="text-gray-300">При заказе от 5 000 ₽</p>
            </div>
            <div>
              <div className="text-5xl mb-4">✅</div>
              <h3 className="text-xl font-bold mb-2">Гарантия качества</h3>
              <p className="text-gray-300">12 месяцев на все товары</p>
            </div>
            <div>
              <div className="text-5xl mb-4">⭐</div>
              <h3 className="text-xl font-bold mb-2">Только оригиналы</h3>
              <p className="text-gray-300">Сертифицированная продукция</p>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-8">
        <div className="container mx-auto px-4 text-center">
          <p className="text-gray-400">© 2024 Knife Store. Все права защищены.</p>
          <p className="text-sm text-gray-500 mt-2">API: http://localhost:8001/docs</p>
        </div>
      </footer>
    </div>
  );
}
