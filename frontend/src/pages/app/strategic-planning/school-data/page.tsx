'use client';

import { useState, useEffect } from 'react';
import { 
  Building, 
  Monitor,
  Wrench,
  TrendingUp,
  AlertCircle,
  CheckCircle,
  Clock
} from '@/icons/nexture';
import { SPCard, SPLoading, SPTable } from '@/components/strategic-planning';
import { useStrategicPlanning } from '@/context/StrategicPlanningContext';

export default function SchoolDataPage() {
  const { getSchoolDataForSWOT, getDigitalReadinessAssessment, getSarprasPrioritization } = useStrategicPlanning();
  const [loading, setLoading] = useState(true);
  const [schoolData, setSchoolData] = useState<any>(null);
  const [digitalReadiness, setDigitalReadiness] = useState<any>(null);
  const [sarprasPriorities, setSarprasPriorities] = useState<any>(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    try {
      const schoolId = 'default-school-id';
      
      const [schoolDataResult, digitalResult, sarprasResult] = await Promise.all([
        getSchoolDataForSWOT(schoolId),
        getDigitalReadinessAssessment(schoolId),
        getSarprasPrioritization(schoolId)
      ]);

      setSchoolData(schoolDataResult);
      setDigitalReadiness(digitalResult);
      setSarprasPriorities(sarprasResult);
    } catch (error) {
      console.error('Error loading school data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <SPLoading />;
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Inventarisasi Sarpras & IT</h1>
        <p className="text-gray-600 mt-1">Analisis kesiapan sarana prasarana dan kesiapan digital sekolah</p>
      </div>

      {/* Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <SPCard
          icon={<Building className="w-5 h-5" />}
          title="Kesiapan Infrastruktur"
          value={schoolData?.infrastructure_data?.classroom_condition?.good_rate || 0}
          subtitle="% ruang kelas baik"
        />
        <SPCard
          icon={<Monitor className="w-5 h-5" />}
          title="Kesiapan Digital"
          value={digitalReadiness?.overall_readiness_score || 0}
          subtitle="Skor kesiapan digital"
        />
        <SPCard
          icon={<Wrench className="w-5 h-5" />}
          title="Kebutuhan Perbaikan"
          value={sarprasPriorities?.length || 0}
          subtitle="Item prioritas"
        />
        <SPCard
          icon={<TrendingUp className="w-5 h-5" />}
          title="Tren Kualitas"
          value="+5%"
          subtitle="Peningkatan tahun ini"
        />
      </div>

      {/* Infrastructure Analysis */}
      <SPCard title="Analisis Infrastruktur">
        <div className="space-y-6">
          {/* Classroom Condition */}
          <div className="p-4 bg-gray-50 rounded-lg">
            <h3 className="font-semibold mb-3">Kondisi Ruang Kelas</h3>
            <div className="grid grid-cols-3 gap-4">
              <div className="text-center">
                <p className="text-2xl font-bold text-green-600">
                  {schoolData?.infrastructure_data?.classroom_condition?.good || 0}
                </p>
                <p className="text-sm text-gray-600">Baik</p>
              </div>
              <div className="text-center">
                <p className="text-2xl font-bold text-yellow-600">
                  {schoolData?.infrastructure_data?.classroom_condition?.damaged || 0}
                </p>
                <p className="text-sm text-gray-600">Rusak</p>
              </div>
              <div className="text-center">
                <p className="text-2xl font-bold">
                  {schoolData?.infrastructure_data?.classroom_condition?.good_rate || 0}%
                </p>
                <p className="text-sm text-gray-600">Tingkat Kelayakan</p>
              </div>
            </div>
          </div>

          {/* Facility Availability */}
          <div>
            <h3 className="font-semibold mb-3">Ketersediaan Fasilitas</h3>
            <div className="space-y-2">
              {schoolData?.infrastructure_data?.facility_availability && (
                <>
                  <div className="flex items-center justify-between p-3 bg-white border rounded">
                    <span>Perpustakaan</span>
                    <span className={`px-2 py-1 rounded text-xs ${
                      schoolData.infrastructure_data.facility_availability.library?.available 
                        ? 'bg-green-100 text-green-800' 
                        : 'bg-red-100 text-red-800'
                    }`}>
                      {schoolData.infrastructure_data.facility_availability.library?.available ? 'Tersedia' : 'Tidak Tersedia'}
                    </span>
                  </div>
                  <div className="flex items-center justify-between p-3 bg-white border rounded">
                    <span>Toilet Siswa</span>
                    <span className={`px-2 py-1 rounded text-xs ${
                      schoolData.infrastructure_data.facility_availability.toilets?.available 
                        ? 'bg-green-100 text-green-800' 
                        : 'bg-red-100 text-red-800'
                    }`}>
                      {schoolData.infrastructure_data.facility_availability.toilets?.available ? 'Tersedia' : 'Tidak Tersedia'}
                    </span>
                  </div>
                </>
              )}
            </div>
          </div>

          {/* Maintenance Needs */}
          <div>
            <h3 className="font-semibold mb-3">Kebutuhan Pemeliharaan</h3>
            <div className="space-y-2">
              {schoolData?.infrastructure_data?.maintenance_needs?.map((need: any) => (
                <div key={need.item} className="p-3 bg-orange-50 border border-orange-200 rounded">
                  <div className="flex items-center justify-between mb-1">
                    <span className="font-medium">{need.item}</span>
                    <span className="text-orange-600 font-semibold">
                      Rp {(need.estimated_cost / 1000000).toFixed(1)}jt
                    </span>
                  </div>
                  <p className="text-sm text-gray-600">{need.timeline}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </SPCard>

      {/* Digital Readiness Assessment */}
      <SPCard title="Penilaian Kesiapan Digital">
        <div className="space-y-6">
          {/* Overall Score */}
          <div className="text-center p-6 bg-gradient-to-r from-purple-50 to-blue-50 rounded-lg">
            <p className="text-sm text-gray-600 mb-2">Skor Kesiapan Digital Overall</p>
            <p className="text-4xl font-bold text-purple-600">
              {digitalReadiness?.overall_readiness_score || 0}
            </p>
            <span className={`inline-block mt-2 px-3 py-1 rounded-full text-sm font-medium ${
              digitalReadiness?.readiness_level === 'ADVANCED' ? 'bg-green-100 text-green-800' :
              digitalReadiness?.readiness_level === 'PROFICIENT' ? 'bg-blue-100 text-blue-800' :
              digitalReadiness?.readiness_level === 'DEVELOPING' ? 'bg-yellow-100 text-yellow-800' :
              'bg-red-100 text-red-800'
            }`}>
              {digitalReadiness?.readiness_level}
            </span>
          </div>

          {/* Assessment Areas */}
          <div className="space-y-4">
            {digitalReadiness?.assessment_areas?.map((area: any) => (
              <div key={area.area} className="p-4 border rounded-lg">
                <div className="flex items-center justify-between mb-2">
                  <h3 className="font-semibold">{area.area}</h3>
                  <span className="text-lg font-bold text-purple-600">{area.score}</span>
                </div>
                <p className="text-sm text-gray-600 mb-2">{area.level}</p>
                <div className="flex flex-wrap gap-2">
                  {area.gaps.map((gap: string) => (
                    <span key={gap} className="px-2 py-1 bg-red-100 text-red-800 rounded text-xs">
                      Gap: {gap}
                    </span>
                  ))}
                  {area.strengths.map((strength: string) => (
                    <span key={strength} className="px-2 py-1 bg-green-100 text-green-800 rounded text-xs">
                      {strength}
                    </span>
                  ))}
                </div>
              </div>
            ))}
          </div>

          {/* Coding & AI Readiness */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="p-4 border rounded-lg">
              <h3 className="font-semibold mb-2">Kesiapan Coding</h3>
              <p className="text-2xl font-bold text-purple-600 mb-1">
                {digitalReadiness?.coding_readiness?.score || 0}
              </p>
              <p className="text-sm text-gray-600">{digitalReadiness?.coding_readiness?.level}</p>
            </div>
            <div className="p-4 border rounded-lg">
              <h3 className="font-semibold mb-2">Kesiapan AI</h3>
              <p className="text-2xl font-bold text-purple-600 mb-1">
                {digitalReadiness?.ai_readiness?.score || 0}
              </p>
              <p className="text-sm text-gray-600">{digitalReadiness?.ai_readiness?.level}</p>
            </div>
          </div>
        </div>
      </SPCard>

      {/* Sarpras Prioritization */}
      <SPCard title="Prioritas Sarpras">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b">
                <th className="text-left p-3">Item</th>
                <th className="text-left p-3">Kondisi Saat Ini</th>
                <th className="text-left p-3">Priority</th>
                <th className="text-left p-3">Biaya</th>
                <th className="text-left p-3">Timeline</th>
                <th className="text-left p-3">Status</th>
              </tr>
            </thead>
            <tbody>
              {sarprasPriorities?.map((item: any) => (
                <tr key={item.item_name} className="border-b">
                  <td className="p-3 font-medium">{item.item_name}</td>
                  <td className="p-3">{item.current_condition}</td>
                  <td className="p-3">
                    <span className={`px-2 py-1 rounded text-xs ${
                      item.priority_level === 'CRITICAL' ? 'bg-red-100 text-red-800' :
                      item.priority_level === 'HIGH' ? 'bg-orange-100 text-orange-800' :
                      item.priority_level === 'MEDIUM' ? 'bg-yellow-100 text-yellow-800' :
                      'bg-green-100 text-green-800'
                    }`}>
                      {item.priority_level}
                    </span>
                  </td>
                  <td className="p-3">Rp {(item.estimated_cost / 1000000).toFixed(1)}jt</td>
                  <td className="p-3">{item.timeline}</td>
                  <td className="p-3">
                    <span className={`px-2 py-1 rounded text-xs flex items-center gap-1 ${
                      item.urgency === 'HIGH' ? 'bg-red-100 text-red-800' :
                      'bg-yellow-100 text-yellow-800'
                    }`}>
                      {item.urgency === 'HIGH' ? <AlertCircle className="w-3 h-3" /> : <Clock className="w-3 h-3" />}
                      {item.urgency}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </SPCard>

      {/* Recommendations */}
      <SPCard title="Rekomendasi">
        <div className="space-y-2">
          {digitalReadiness?.recommendations?.map((rec: string, index: number) => (
            <div key={index} className="flex items-start gap-2 p-3 bg-blue-50 rounded-lg">
              <CheckCircle className="w-4 h-4 text-blue-600 mt-0.5" />
              <p className="text-sm">{rec}</p>
            </div>
          ))}
        </div>
      </SPCard>
    </div>
  );
}