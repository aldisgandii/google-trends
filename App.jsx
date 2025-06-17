import { useState, useEffect } from 'react'
import { Search, Calendar, Filter } from 'lucide-react'
import { Button } from '@/components/ui/button.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Card, CardContent } from '@/components/ui/card.jsx'
import './App.css'

function App() {
  const [trends, setTrends] = useState([])
  const [loading, setLoading] = useState(false)
  const [keyword, setKeyword] = useState('')
  const [selectedDate, setSelectedDate] = useState('')
  const [timeframe, setTimeframe] = useState('today 1-d')

  const fetchTrends = async () => {
    setLoading(true)
    try {
      const params = new URLSearchParams()
      if (keyword) params.append('keyword', keyword)
      if (selectedDate) params.append('date', selectedDate)
      params.append('timeframe', timeframe)

      const response = await fetch(`https://9yhyi3cq8v7z.manus.space/api/trends?${params}`)
      const data = await response.json()
      
      if (data.success) {
        setTrends(data.data)
      }
    } catch (error) {
      console.error('Error fetching trends:', error)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchTrends()
  }, [])

  const handleSearch = () => {
    fetchTrends()
  }

  const getGridSize = (index, interest) => {
    // Variasi ukuran grid berdasarkan interest dan posisi
    if (interest > 80) return 'col-span-2 row-span-2'
    if (interest > 60) return 'col-span-2 row-span-1'
    if (interest > 40) return 'col-span-1 row-span-2'
    return 'col-span-1 row-span-1'
  }

  const formatDate = () => {
    return new Date().toLocaleDateString('id-ID', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    })
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Google Trends Indonesia</h1>
              <p className="text-gray-600 mt-1">{formatDate()}</p>
            </div>
            <div className="flex items-center space-x-2">
              <div className="text-sm text-gray-500">
                Total Keywords: {trends.length}
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Filter Panel */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <Card className="mb-6">
          <CardContent className="p-6">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              {/* Keyword Filter */}
              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-700">
                  <Search className="inline w-4 h-4 mr-1" />
                  Cari Keyword
                </label>
                <Input
                  type="text"
                  placeholder="Masukkan keyword..."
                  value={keyword}
                  onChange={(e) => setKeyword(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                />
              </div>

              {/* Date Filter */}
              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-700">
                  <Calendar className="inline w-4 h-4 mr-1" />
                  Tanggal
                </label>
                <Input
                  type="date"
                  value={selectedDate}
                  onChange={(e) => setSelectedDate(e.target.value)}
                />
              </div>

              {/* Timeframe Filter */}
              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-700">
                  <Filter className="inline w-4 h-4 mr-1" />
                  Periode
                </label>
                <select
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  value={timeframe}
                  onChange={(e) => setTimeframe(e.target.value)}
                >
                  <option value="today 1-d">Hari Ini</option>
                  <option value="today 7-d">7 Hari Terakhir</option>
                  <option value="today 1-m">1 Bulan Terakhir</option>
                  <option value="today 3-m">3 Bulan Terakhir</option>
                </select>
              </div>

              {/* Search Button */}
              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-700 opacity-0">
                  Action
                </label>
                <Button 
                  onClick={handleSearch}
                  disabled={loading}
                  className="w-full"
                >
                  {loading ? 'Loading...' : 'Cari Trends'}
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Trends Grid */}
        {loading ? (
          <div className="flex justify-center items-center h-64">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          </div>
        ) : (
          <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-2 auto-rows-[120px]">
            {trends.map((trend, index) => (
              <div
                key={index}
                className={`${getGridSize(index, trend.interest)} rounded-lg p-4 flex flex-col justify-between text-white font-medium shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105 cursor-pointer`}
                style={{ backgroundColor: trend.color }}
              >
                <div className="flex-1 flex items-center justify-center">
                  <span className="text-center text-sm md:text-base lg:text-lg font-semibold leading-tight">
                    {trend.keyword}
                  </span>
                </div>
                <div className="text-xs opacity-80 text-center">
                  Interest: {trend.interest}
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Empty State */}
        {!loading && trends.length === 0 && (
          <div className="text-center py-12">
            <div className="text-gray-400 text-lg mb-2">Tidak ada data trends ditemukan</div>
            <p className="text-gray-500">Coba ubah filter atau keyword pencarian</p>
          </div>
        )}
      </div>

      {/* Footer */}
      <footer className="bg-white border-t mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="text-center text-gray-500 text-sm">
            <p>Data dari Google Trends Indonesia • Diperbarui secara real-time</p>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default App

