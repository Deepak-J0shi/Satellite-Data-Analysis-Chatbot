import { Pin, ExternalLink } from "lucide-react";

export default function AnalysisCard({ data }) {

  const {
    preview_url,
    dataset_info,
    methodology,
    interpretation,
    legend,
  } = data;

  return (
    <div className="bg-white dark:bg-[#111827] border border-slate-200 dark:border-slate-800 rounded-2xl p-6">

      {/* REPORT HEADER */}

      <div className="mb-6 border-b border-slate-200 dark:border-slate-800 pb-4">

        <h2 className="text-2xl font-bold text-slate-900 dark:text-white">

          NDVI Vegetation Analysis

        </h2>

        <div className="mt-3 flex flex-wrap gap-6 text-sm text-slate-500">

          <div>
            <span className="font-semibold">
              Satellite:
            </span>{" "}
            {dataset_info?.dataset_name}
          </div>

          <div>
            <span className="font-semibold">
              Resolution:
            </span>{" "}
            {dataset_info?.resolution}
          </div>

          <div>
            <span className="font-semibold">
              Period:
            </span>{" "}
            {dataset_info?.date_range}
          </div>

        </div>

      </div>

      {/* MAIN GRID */}

      <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">

        {/* LEFT */}

        <div className="space-y-4">

          <div className="bg-slate-50 dark:bg-slate-900 rounded-xl p-4">

            <h3 className="font-semibold mb-3">

              Dataset Information

            </h3>

            <div className="space-y-2 text-sm">

              <div>

                <strong>Dataset:</strong>{" "}
                {dataset_info?.dataset_name}

              </div>

              <div>

                <strong>Collection:</strong>{" "}
                {dataset_info?.gee_collection}

              </div>

              <div>

                <strong>Date Range:</strong>{" "}
                {dataset_info?.date_range}

              </div>

            </div>

          </div>

          {dataset_info?.bands_used && (

            <div className="bg-slate-50 dark:bg-slate-900 rounded-xl p-4">

              <h3 className="font-semibold mb-3">

                Bands Used

              </h3>

              <div className="flex flex-wrap gap-2">

                {dataset_info.bands_used.map((band) => (

                  <span
                    key={band}
                    className="px-3 py-1 rounded-full bg-blue-100 dark:bg-blue-900 text-sm"
                  >
                    {band}
                  </span>

                ))}

              </div>

            </div>

          )}

          {legend && (

            <div className="bg-slate-50 dark:bg-slate-900 rounded-xl p-4">

              <h3 className="font-semibold mb-3">

                Legend

              </h3>

              <div className="space-y-2">

                {Object.entries(legend).map(([color, text]) => (

                  <div
                    key={color}
                    className="flex justify-between text-sm"
                  >

                    <span className="font-medium">
                      {color}
                    </span>

                    <span>
                      {text}
                    </span>

                  </div>

                ))}

              </div>

            </div>

          )}

        </div>

        {/* RIGHT */}

        <div>

          {preview_url && (

            <div className="rounded-xl overflow-hidden border border-slate-200 dark:border-slate-800">

              <img
                src={preview_url}
                alt="Satellite Analysis"
                className="w-full object-cover"
              />

            </div>

          )}

          <div className="mt-4 flex gap-3">

            <button
              onClick={() => window.open(preview_url)}
              className="flex items-center gap-2 px-4 py-2 rounded-xl bg-blue-600 text-white"
            >

              <ExternalLink size={16} />

              Open Interactive Map

            </button>

            <button
              className="flex items-center gap-2 px-4 py-2 rounded-xl border"
            >

              <Pin size={16} />

              Pin

            </button>

          </div>

        </div>

      </div>

      {/* SUMMARY */}

      <div className="mt-6 grid grid-cols-1 xl:grid-cols-2 gap-4">

        <div className="bg-slate-50 dark:bg-slate-900 rounded-xl p-4">

          <h3 className="font-semibold mb-3">

            Methodology

          </h3>

          <p className="text-sm leading-6">

            {methodology}

          </p>

        </div>

        <div className="bg-slate-50 dark:bg-slate-900 rounded-xl p-4">

          <h3 className="font-semibold mb-3">

            Interpretation

          </h3>

          <p className="text-sm leading-6">

            {interpretation}

          </p>

        </div>

      </div>

    </div>
  );
}