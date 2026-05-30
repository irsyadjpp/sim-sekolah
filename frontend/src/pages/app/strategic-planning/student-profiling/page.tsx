'use client';

import { useState, useEffect } from 'react';
import {
  School as SchoolIcon,
  Group as UsersIcon,
  TrendingUp as TrendingUpIcon,
  Warning as AlertTriangleIcon,
  Download as DownloadIcon,
  FilterList as FilterListIcon,
  BarChart as BarChartIcon,
  PieChart as PieChartIcon
} from '@mui/icons-material';
import { SPCard, SPTable, SPLoading, SPEmptyState } from '@/components/strategic-planning';
import { useStrategicPlanning } from '@/context/StrategicPlanningContext';

export default function StudentProfilingPage() {
  const { getStudentProfileAnalysis, getStatisticalAnalysis, generateActionPlanRecommendations } = useStrategicPlanning();
  const [loading, setLoading] = useState(true);
  const [selectedProfile, setSelectedProfile] = useState('BERIMAN');
  const [analysisData, setAnalysisData] = useState<any>(null);
  const [statisticalData, setStatisticalData] = useState<any>(null);
  const [recommendations, setRecommendations] = useState<any>(null);

  useEffect(() => {
    loadAnalysisData();
  }, [selectedProfile]);

  const loadAnalysisData = async () => {
    setLoading(true);
    try {
      // Get school ID from context or use default
      const schoolId = 'default-school-id';

      const [profileData, statsData, actionPlans] = await Promise.all([
        getStudentProfileAnalysis(schoolId, selectedProfile),
        getStatisticalAnalysis(schoolId, 'correlation'),
        generateActionPlanRecommendations(schoolId)
      ]);

      setAnalysisData(profileData);
      setStatisticalData(statsData);
      setRecommendations(actionPlans);
    } catch (error) {
      console.error('Error loading analysis data:', error);
    } finally {
      setLoading(false);
    }
  };

  const profiles = [
    { code: 'BERIMAN', name: 'Beriman & Bertakwa' },
    { code: 'BERGOTONG_ROYONG', name: 'Bergotong Royong' },
    { code: 'MANDIRI', name: 'Mandiri' },
    { code: 'BERNALAR_KRITIS', name: 'Bernalar Kritis' },
    { code: 'KREATIF', name: 'Kreatif' },
  ];

  if (loading) {
    return <SPLoading />;
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Profiling Kebutuhan Murid</h1>
          <p className="text-gray-600 mt-1">Analisis mendalam profil dan kebutuhan siswa untuk pembelajaran berdiferensiasi</p>
        </div>
        <div className="flex gap-2">
          <button className="flex items-center gap-2 px-4 py-2 bg-white border border-gray-300 rounded-lg hover:bg-gray-50">
            <FilterListIcon className="w-4 h-4" />
            Filter
          </button>
          <button className="flex items-center gap-2 px-4 py-2 bg-white border border-gray-300 rounded-lg hover:bg-gray-50">
            <DownloadIcon className="w-4 h-4" />
            Export
          </button>
        </div>
      </div>

      {/* Profile Selection */}
      <div className="flex gap-2 overflow-x-auto pb-2">
        {profiles.map((profile) => (
          <button
            key={profile.code}
            onClick={() => setSelectedProfile(profile.code)}
            className={`px-4 py-2 rounded-lg whitespace-nowrap ${selectedProfile === profile.code
              ? 'bg-purple-600 text-white'
              : 'bg-white text-gray-700 border border-gray-300 hover:bg-gray-50'
              }`}
          >
            {profile.name}
          </button>
        ))}
      </div>

      {/* Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <SPCard
          icon={<UsersIcon className="w-5 h-5" />}
          title="Total Siswa"
          value={analysisData?.total_students || 0}
          subtitle="Siswa aktif"
        />
        <SPCard
          icon={<TrendingUpIcon className="w-5 h-5" />}
          title="Tren Profil"
          value="+15%"
          subtitle="Peningkatan bulan ini"
        />
        <SPCard
          icon={<BarChartIcon className="w-5 h-5" />}
          title="Distribusi Profil"
          value="Seimbang"
          subtitle="Across all dimensions"
        />
        <SPCard
          icon={<AlertTriangleIcon className="w-5 h-5" />}
          title="Faktor Risiko"
          value={analysisData?.risk_factors?.length || 0}
          subtitle="Butuh perhatian"
        />
      </div>

      {/* Profile Distribution Chart */}
      <SPCard title="Distribusi Profil Siswa">
        <div className="space-y-4">
          {analysisData?.profile_distribution?.map((dist: any) => (
            <div key={dist.profile_level} className="flex items-center gap-4">
              <div className="w-32 text-sm font-medium">{dist.profile_level}</div>
              <div className="flex-1 bg-gray-200 rounded-full h-4">
                <div
                  className="bg-purple-600 h-4 rounded-full transition-all"
                  style={{ width: `${dist.percentage}%` }}
                />
              </div>
              <div className="w-20 text-right text-sm">{dist.count} ({dist.percentage.toFixed(1)}%)</div>
            </div>
          ))}
        </div>
      </SPCard>

      {/* Risk Factors */}
      <SPCard title="Faktor Risiko yang Teridentifikasi">
        <div className="space-y-4">
          {analysisData?.risk_factors?.map((risk: any) => (
            <div key={risk.factor} className="p-4 border border-gray-200 rounded-lg">
              <div className="flex items-center justify-between mb-2">
                <h3 className="font-semibold">{risk.factor}</h3>
                <span className={`px-2 py-1 rounded text-xs font-medium ${risk.severity === 'HIGH' ? 'bg-red-100 text-red-800' :
                  risk.severity === 'MEDIUM' ? 'bg-yellow-100 text-yellow-800' :
                    'bg-green-100 text-green-800'
                  }`}>
                  {risk.severity}
                </span>
              </div>
              <p className="text-sm text-gray-600 mb-2">
                {risk.affected_count} siswa ({risk.percentage.toFixed(1)}%)
              </p>
              <p className="text-sm font-medium text-purple-600">
                Mitigasi: {risk.mitigation}
              </p>
            </div>
          ))}
        </div>
      </SPCard>

      {/* Action Plan Recommendations */}
      <SPCard title="Rekomendasi Rencana Aksi">
        <div className="space-y-4">
          {recommendations?.map((rec: any) => (
            <div key={rec.id} className="p-4 border border-gray-200 rounded-lg">
              <div className="flex items-start justify-between mb-2">
                <h3 className="font-semibold">{rec.action}</h3>
                <span className={`px-2 py-1 rounded text-xs font-medium ${rec.priority === 1 ? 'bg-red-100 text-red-800' :
                  rec.priority === 2 ? 'bg-yellow-100 text-yellow-800' :
                    'bg-green-100 text-green-800'
                  }`}>
                  Priority {rec.priority}
                </span>
              </div>
              <p className="text-sm text-gray-600 mb-2">{rec.expected_outcome}</p>
              <div className="flex gap-4 text-xs text-gray-500">
                <span>Timeline: {rec.timeline}</span>
                <span>Responsible: {rec.responsible}</span>
              </div>
            </div>
          ))}
        </div>
      </SPCard>

      {/* Statistical Analysis */}
      <SPCard title="Analisis Statistik">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="p-4 bg-gray-50 rounded-lg">
            <h3 className="font-semibold mb-2">Korelasi Literasi-Numerasi</h3>
            <p className="text-2xl font-bold text-purple-600">
              {statisticalData?.results?.correlation_analysis?.literacy_vs_numeracy || 0}
            </p>
            <p className="text-sm text-gray-600">Korelasi positif yang kuat</p>
          </div>
          <div className="p-4 bg-gray-50 rounded-lg">
            <h3 className="font-semibold mb-2">Korelasi Kehadiran-Performa</h3>
            <p className="text-2xl font-bold text-purple-600">
              {statisticalData?.results?.correlation_analysis?.attendance_vs_performance || 0}
            </p>
            <p className="text-sm text-gray-600">Pengaruh signifikan kehadiran</p>
          </div>
        </div>
      </SPCard>
    </div>
  );
}