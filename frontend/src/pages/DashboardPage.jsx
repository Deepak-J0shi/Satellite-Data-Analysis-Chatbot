import {
  MoreVertical,
  Download,
  Maximize2,
  Pin,
} from "lucide-react";

export default function DashboardPage() {

  return (

    <div className="h-screen overflow-y-auto bg-slate-50 dark:bg-[#0f172a] transition-all duration-300">

      {/* Header */}
      <div className="bg-white dark:bg-[#111827] border-b border-slate-200 dark:border-slate-800 px-8 py-5">

        <div className="max-w-7xl mx-auto flex items-center justify-between">

          <div>

            <h1 className="text-3xl font-semibold tracking-tight text-slate-900 dark:text-white">
              Analysis Dashboard
            </h1>

            <p className="text-slate-500 dark:text-slate-400 mt-1">
              Saved charts, reports, previews and satellite insights
            </p>

          </div>

          <button className="bg-blue-600 hover:bg-blue-700 text-white px-5 py-3 rounded-xl transition-all">
            New Dashboard
          </button>

        </div>

      </div>

      {/* Grid */}
      <div className="p-8">

        <div className="max-w-7xl mx-auto grid grid-cols-2 gap-6">

          <DashboardCard title="NDVI Trend Analysis">
            <ChartPlaceholder label="NDVI Temporal Chart" />
          </DashboardCard>

          <DashboardCard title="Flood Mapping Result">
            <ChartPlaceholder label="Flood Detection Map" />
          </DashboardCard>

          <DashboardCard title="Urban Heat Island">
            <ChartPlaceholder label="Heatmap Visualization" />
          </DashboardCard>

          <DashboardCard title="Land Cover Distribution">
            <ChartPlaceholder label="Land Cover Pie Chart" />
          </DashboardCard>

          <div className="col-span-2">

            <DashboardCard title="Satellite Preview Workspace">

              <div className="h-[500px] rounded-2xl border border-slate-200 dark:border-slate-800 bg-slate-100 dark:bg-[#0b1220] flex items-center justify-center text-slate-400">
                Leaflet Map / Satellite Tile Preview
              </div>

            </DashboardCard>

          </div>

        </div>

      </div>

    </div>
  );
}

function DashboardCard({ title, children }) {

  return (

    <div className="bg-white dark:bg-[#111827] border border-slate-200 dark:border-slate-800 rounded-2xl overflow-hidden transition-all duration-300">

      {/* Header */}
      <div className="px-5 py-4 border-b border-slate-200 dark:border-slate-800 flex items-center justify-between">

        <h2 className="font-semibold text-slate-900 dark:text-white">
          {title}
        </h2>

        <div className="flex items-center gap-2">

          <ActionButton icon={<Pin size={15} />} />
          <ActionButton icon={<Download size={15} />} />
          <ActionButton icon={<Maximize2 size={15} />} />
          <ActionButton icon={<MoreVertical size={15} />} />

        </div>

      </div>

      {/* Content */}
      <div className="p-5">
        {children}
      </div>

    </div>
  );
}

function ActionButton({ icon }) {

  return (

    <button className="p-2 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-500 dark:text-slate-400 transition-all">

      {icon}

    </button>
  );
}

function ChartPlaceholder({ label }) {

  return (

    <div className="h-[320px] rounded-2xl border border-slate-200 dark:border-slate-800 bg-slate-100 dark:bg-[#0b1220] flex items-center justify-center text-slate-400">

      {label}

    </div>
  );
}