import Image from "next/image"
import Link from "next/link"
import { Button } from "@/components/ui/button"

export default function HomePage() {
  return (
    <div className="relative min-h-screen flex flex-col items-center justify-between p-6 text-white overflow-hidden">
      {/* Diagonal stripes overlay */}
      <div className="absolute inset-0 z-0 pointer-events-none bg-gradient-to-b from-black to-red-900">
        <div className="absolute inset-0 bg-[repeating-linear-gradient(135deg,rgba(0,0,0,0.15)_0_40px,transparent_40px,transparent_80px)]" />
      </div>

      {/* Header Logo */}
      <div className="w-full flex justify-center pt-8 z-10">
        {/* If you have an SVG for the logo, use it here for best match */}
        <span className="text-5xl font-extrabold tracking-tight" style={{ fontFamily: "sans-serif" }}>
          Ex<span className="text-red-500">x</span>on
        </span>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col items-center justify-center space-y-8 z-10">
        {/* Robot Character */}
        <div className="relative">
          <Image
            src="/robot.png"
            alt="Exon AI Robot"
            width={500}
            height={600}
            className="drop-shadow-[0_8px_32px_rgba(0,0,0,0.5)]"
            priority
          />
        </div>

        {/* Welcome Text */}
        <div className="text-center space-y-2">
          <h2 className="text-3xl font-bold tracking-wide">Ready to manage</h2>
          <h2 className="text-3xl font-bold tracking-wide">today's?</h2>
        </div>
      </div>

      {/* Get Started Button */}
      <div className="w-full max-w-sm z-10 pb-8">
        <Link href="/dashboard">
          <Button className="w-full bg-black/70 hover:bg-black text-white border-none rounded-full py-3 text-lg font-semibold shadow-lg transition">
            Get started
          </Button>
        </Link>
      </div>
    </div>
  )
}
