import { Outlet, NavLink } from "react-router-dom";

import {
  MessageSquare,
  LayoutDashboard,
  BookOpen,
  Plus,
  Moon,
  Sun,
} from "lucide-react";

import { useTheme } from "../context/ThemeContext";

export default function MainLayout() {

  const { theme, toggleTheme } = useTheme();

  return (

    <div className="flex h-screen bg-slate-50 dark:bg-[#0f172a] text-slate-900 dark:text-slate-100 transition-all duration-300">

      {/* Sidebar */}
      <aside className="w-80 bg-white dark:bg-[#111827] border-r border-slate-200 dark:border-slate-800 flex flex-col transition-all duration-300">

        {/* Logo */}
        {/* Logo */}
<div className="px-6 py-6 border-b border-slate-200 dark:border-slate-800">

  <h1 className="text-2xl font-bold tracking-tight text-slate-900 dark:text-white">
    GeoVision AI
  </h1>

  <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">
    Geospatial Intelligence Platform
  </p>

</div>

        {/* Theme Toggle */}
        <div className="p-4">

          <button
            onClick={toggleTheme}
            className="w-full flex items-center justify-center gap-2 border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 hover:bg-slate-100 dark:hover:bg-slate-700 py-3 rounded-xl transition-all duration-300"
          >

            {theme === "dark" ? (
              <>
                <Sun size={18} />
                Light Mode
              </>
            ) : (
              <>
                <Moon size={18} />
                Dark Mode
              </>
            )}

          </button>

        </div>

        {/* New Analysis */}
        <div className="px-4">

          <button className="w-full flex items-center justify-center gap-2 bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-xl transition-all">

            <Plus size={18} />
            New Analysis

          </button>

        </div>

        {/* Navigation */}
        <nav className="px-4 mt-6 space-y-2">

          <SidebarItem
            to="/"
            icon={<MessageSquare size={18} />}
            label="AI Chat"
          />

          <SidebarItem
            to="/dashboard"
            icon={<LayoutDashboard size={18} />}
            label="Dashboard"
          />

          <SidebarItem
            to="/docs"
            icon={<BookOpen size={18} />}
            label="Documentation"
          />

        </nav>

        {/* Recent Analyses */}
        <div className="px-4 mt-8 flex-1 overflow-y-auto">

          <h3 className="text-xs uppercase tracking-wide text-slate-400 dark:text-slate-500 mb-4">
            Saved Analyses
          </h3>

          <div className="space-y-2">

            <RecentItem title="NDVI Uttarakhand 2023" />
            <RecentItem title="Flood Mapping Assam" />
            <RecentItem title="Urban Heat Delhi" />
            <RecentItem title="Land Cover Change" />

          </div>

        </div>

        {/* Footer */}
        <div className="p-4 border-t border-slate-200 dark:border-slate-800 text-xs text-slate-400 dark:text-slate-500">

          React + Tailwind + Leaflet

        </div>

      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-hidden">

        <Outlet />

      </main>

    </div>
  );
}

function SidebarItem({ to, icon, label }) {

  return (

    <NavLink
      to={to}
      className={({ isActive }) =>
        `flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-300 ${
          isActive
            ? "bg-blue-50 dark:bg-slate-800 text-blue-700 dark:text-white"
            : "hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-300"
        }`
      }
    >

      {icon}

      <span className="font-medium">
        {label}
      </span>

    </NavLink>
  );
}

function RecentItem({ title }) {

  return (

    <div className="px-4 py-3 rounded-xl hover:bg-slate-100 dark:hover:bg-slate-800 cursor-pointer transition-all duration-300">

      <p className="text-sm text-slate-700 dark:text-slate-300 truncate">
        {title}
      </p>

    </div>
  );
}