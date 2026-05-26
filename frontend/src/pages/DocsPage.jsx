const datasets = [
  {
    name: "LANDSAT_8",
    description:
      "Medium-resolution multispectral satellite used for vegetation, urban heat, land cover and environmental monitoring.",
    analyses: [
      "NDVI",
      "EVI",
      "NDWI",
      "LAND_COVER",
      "URBAN_HEAT",
      "BURN_AREA",
      "TIMESERIES",
    ],
  },

  {
    name: "LANDSAT_9",
    description:
      "Latest Landsat mission providing improved radiometric performance for long-term Earth observation analysis.",
    analyses: [
      "NDVI",
      "EVI",
      "NDWI",
      "LAND_COVER",
      "URBAN_HEAT",
      "BURN_AREA",
      "TIMESERIES",
    ],
  },

  {
    name: "SENTINEL_1",
    description:
      "Synthetic Aperture Radar satellite capable of monitoring Earth surfaces through clouds and at night.",
    analyses: [
      "SAR",
      "FLOOD",
      "LAND_COVER",
      "TIMESERIES",
    ],
  },

  {
    name: "SENTINEL_2",
    description:
      "High-resolution optical imagery for vegetation, water bodies and environmental analysis.",
    analyses: [
      "NDVI",
      "EVI",
      "NDWI",
      "LAND_COVER",
      "FLOOD",
      "BURN_AREA",
      "TIMESERIES",
    ],
  },

  {
    name: "MODIS",
    description:
      "Moderate-resolution global dataset optimized for climate and long-term temporal analysis.",
    analyses: [
      "CLIMATE",
      "NDVI",
      "LAND_COVER",
      "TIMESERIES",
      "URBAN_HEAT",
    ],
  },
];

export default function DocsPage() {

  return (

    <div className="h-screen overflow-y-auto bg-slate-50 dark:bg-[#0f172a] transition-all duration-300">

      {/* Header */}
      <div className="bg-white dark:bg-[#111827] border-b border-slate-200 dark:border-slate-800 px-8 py-6">

        <div className="max-w-6xl mx-auto">

          <h1 className="text-4xl font-semibold tracking-tight text-slate-900 dark:text-white">
            Satellite Data Analysis Chatbot
          </h1>

          <p className="text-slate-600 dark:text-slate-400 mt-3 text-lg leading-8 max-w-4xl">
            An AI-powered geospatial intelligence platform that enables
            users to perform satellite imagery analysis using natural
            language queries powered by modern LLMs and Google Earth Engine.
          </p>

        </div>

      </div>

      {/* Content */}
      <div className="px-8 py-10">

        <div className="max-w-6xl mx-auto space-y-10">

          <Section title="What is this chatbot?">

            <p className="text-slate-600 dark:text-slate-400 leading-8">
              This chatbot is an intelligent satellite data analysis system
              designed to simplify geospatial workflows using natural language.
            </p>

          </Section>

          <Section title="Supported Satellite Datasets">

            <div className="space-y-6 mt-6">

              {datasets.map((dataset) => (

                <div
                  key={dataset.name}
                  className="bg-white dark:bg-[#111827] border border-slate-200 dark:border-slate-800 rounded-2xl p-6 transition-all duration-300"
                >

                  <h3 className="text-2xl font-semibold text-slate-900 dark:text-white">
                    {dataset.name}
                  </h3>

                  <p className="text-slate-600 dark:text-slate-400 mt-3 leading-7 max-w-3xl">
                    {dataset.description}
                  </p>

                  <div className="mt-6 flex flex-wrap gap-3">

                    {dataset.analyses.map((analysis) => (

                      <span
                        key={analysis}
                        className="px-4 py-2 rounded-xl bg-blue-50 dark:bg-slate-800 text-blue-700 dark:text-blue-400 text-sm font-medium"
                      >
                        {analysis}
                      </span>

                    ))}

                  </div>

                </div>
              ))}

            </div>

          </Section>

        </div>

      </div>

    </div>
  );
}

function Section({ title, children }) {

  return (

    <section>

      <h2 className="text-3xl font-semibold tracking-tight text-slate-900 dark:text-white">
        {title}
      </h2>

      <div className="mt-5">
        {children}
      </div>

    </section>
  );
}