export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
      <div className="container mx-auto px-4 py-16">
        <div className="max-w-4xl mx-auto">
          {/* Header */}
          <div className="text-center mb-12">
            <h1 className="text-5xl font-bold text-gray-900 mb-4">
              Welcome to Ad Page
            </h1>
            <p className="text-xl text-gray-600">
              Earn points by watching advertisements and convert them to real money!
            </p>
          </div>

          {/* Features Grid */}
          <div className="grid md:grid-cols-3 gap-6 mb-12">
            <div className="bg-white rounded-lg shadow-lg p-6 border-2 border-blue-100">
              <div className="text-4xl mb-4">💰</div>
              <h3 className="text-xl font-semibold mb-2">Earn Points</h3>
              <p className="text-gray-600">
                Watch ads and earn 10 points instantly with each view
              </p>
            </div>

            <div className="bg-white rounded-lg shadow-lg p-6 border-2 border-green-100">
              <div className="text-4xl mb-4">🎁</div>
              <h3 className="text-xl font-semibold mb-2">Daily Bonus</h3>
              <p className="text-gray-600">
                Get 10 bonus points every day just for logging in
              </p>
            </div>

            <div className="bg-white rounded-lg shadow-lg p-6 border-2 border-purple-100">
              <div className="text-4xl mb-4">💸</div>
              <h3 className="text-xl font-semibold mb-2">Withdraw</h3>
              <p className="text-gray-600">
                Convert 1000 points to ₹10 and withdraw to your account
              </p>
            </div>
          </div>

          {/* CTA Section */}
          <div className="bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg shadow-xl p-8 text-white text-center">
            <h2 className="text-3xl font-bold mb-4">Ready to Start Earning?</h2>
            <p className="text-lg mb-6">
              Join our Telegram bot to start watching ads and earning points today!
            </p>
            <a
              href="https://t.me/YOUR_BOT_USERNAME"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-block bg-white text-blue-600 font-semibold px-8 py-3 rounded-full hover:bg-gray-100 transition-colors"
            >
              Start on Telegram
            </a>
          </div>

          {/* How it Works */}
          <div className="mt-12 bg-white rounded-lg shadow-lg p-8">
            <h2 className="text-2xl font-bold text-center mb-8">How It Works</h2>
            <div className="space-y-4">
              <div className="flex items-start">
                <div className="flex-shrink-0 w-8 h-8 bg-blue-500 text-white rounded-full flex items-center justify-center font-bold mr-4">
                  1
                </div>
                <div>
                  <h3 className="font-semibold text-lg">Join Our Telegram Bot</h3>
                  <p className="text-gray-600">Click the button above to start your journey</p>
                </div>
              </div>

              <div className="flex items-start">
                <div className="flex-shrink-0 w-8 h-8 bg-blue-500 text-white rounded-full flex items-center justify-center font-bold mr-4">
                  2
                </div>
                <div>
                  <h3 className="font-semibold text-lg">Watch Advertisements</h3>
                  <p className="text-gray-600">Click on ads and earn 10 points each time</p>
                </div>
              </div>

              <div className="flex items-start">
                <div className="flex-shrink-0 w-8 h-8 bg-blue-500 text-white rounded-full flex items-center justify-center font-bold mr-4">
                  3
                </div>
                <div>
                  <h3 className="font-semibold text-lg">Accumulate Points</h3>
                  <p className="text-gray-600">Build up your balance to 5000 points minimum</p>
                </div>
              </div>

              <div className="flex items-start">
                <div className="flex-shrink-0 w-8 h-8 bg-blue-500 text-white rounded-full flex items-center justify-center font-bold mr-4">
                  4
                </div>
                <div>
                  <h3 className="font-semibold text-lg">Withdraw Your Earnings</h3>
                  <p className="text-gray-600">Convert points to cash and withdraw via UPI or bank transfer</p>
                </div>
              </div>
            </div>
          </div>

          {/* Stats */}
          <div className="mt-12 grid md:grid-cols-3 gap-6 text-center">
            <div className="bg-blue-50 rounded-lg p-6">
              <div className="text-3xl font-bold text-blue-600">10</div>
              <div className="text-gray-600 mt-2">Points per Ad</div>
            </div>
            <div className="bg-green-50 rounded-lg p-6">
              <div className="text-3xl font-bold text-green-600">₹10</div>
              <div className="text-gray-600 mt-2">per 1000 Points</div>
            </div>
            <div className="bg-purple-50 rounded-lg p-6">
              <div className="text-3xl font-bold text-purple-600">5000</div>
              <div className="text-gray-600 mt-2">Min. Withdrawal</div>
            </div>
          </div>
        </div>
      </div>
    </main>
  )
}
