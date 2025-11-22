import { Card, CardContent } from "@/components/ui/card"
import { TrendingUp, TrendingDown, Truck, Package } from "lucide-react"
import { AppLayout } from "@/components/app-layout"

interface ActivityItem {
  id: number
  type: "inbound" | "outbound"
  date: string
  count: number
  trend: "up" | "down"
}

export default function DashboardPage() {
  const activities: ActivityItem[] = [
    { id: 1, type: "inbound", date: "07/08/25", count: 32, trend: "up" },
    { id: 2, type: "outbound", date: "07/08/25", count: 21, trend: "down" },
    { id: 3, type: "inbound", date: "07/08/25", count: 10, trend: "up" },
  ]

  return (
    <AppLayout>
      <div className="p-4 space-y-6">
        {/* Title */}
        <div className="text-center">
          <h1 className="text-2xl font-semibold text-white">Dashboard</h1>
          <h1 className="text-2xl font-semibold text-white">Trend</h1>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-2 gap-4">
          {/* Inbound Card */}
          <Card className="bg-red-800/50 border-red-700/30 backdrop-blur-sm">
            <CardContent className="p-4 text-center">
              <div className="flex items-center justify-center space-x-2 mb-2">
                <span className="text-4xl font-bold text-white">18.2</span>
                <TrendingUp className="h-6 w-6 text-green-400" />
              </div>
              <p className="text-sm text-white">Inbound</p>
              <p className="text-sm text-white">this week</p>
              <button className="text-xs text-red-400 mt-2 hover:text-red-300">see more</button>
            </CardContent>
          </Card>

          {/* Outbound Card */}
          <Card className="bg-red-800/50 border-red-700/30 backdrop-blur-sm">
            <CardContent className="p-4 text-center">
              <div className="flex items-center justify-center space-x-2 mb-2">
                <span className="text-4xl font-bold text-white">10.9</span>
                <TrendingDown className="h-6 w-6 text-red-400" />
              </div>
              <p className="text-sm text-white">out bound</p>
              <p className="text-sm text-white">this week</p>
              <button className="text-xs text-red-400 mt-2 hover:text-red-300">see more</button>
            </CardContent>
          </Card>
        </div>

        {/* Total Cost Card */}
        <Card className="bg-red-800/50 border-red-700/30 backdrop-blur-sm">
          <CardContent className="p-4 text-center">
            <div className="text-4xl font-bold mb-2 text-white">10327 $</div>
            <p className="text-sm text-white mb-2">Total Cost / month</p>
            <button className="text-xs text-red-400 hover:text-red-300">see more</button>
          </CardContent>
        </Card>

        {/* History Section */}
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-medium text-white">History or Recent Activity</h2>
            <button className="text-xs text-red-400 hover:text-red-300">see more</button>
          </div>

          {/* Activity List */}
          <div className="space-y-3">
            {activities.map((activity) => (
              <Card key={activity.id} className="bg-red-800/50 border-red-700/30 backdrop-blur-sm">
                <CardContent className="p-4 flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <div className="p-2 bg-gradient-to-b from-black to-red-900/80 rounded-lg">
                      {activity.type === "inbound" ? (
                        <Package className="h-5 w-5 text-white" />
                      ) : (
                        <Truck className="h-5 w-5 text-white" />
                      )}
                    </div>
                    <div>
                      <p className="font-medium capitalize text-white">{activity.type}</p>
                      <p className="text-sm text-white">{activity.date}</p>
                    </div>
                  </div>
                  <div className="flex items-center space-x-2">
                    <span className="text-2xl font-bold text-white">{activity.count}</span>
                    {activity.trend === "up" ? (
                      <TrendingUp className="h-5 w-5 text-green-400" />
                    ) : (
                      <TrendingDown className="h-5 w-5 text-red-400" />
                    )}
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </div>
    </AppLayout>
  )
}
