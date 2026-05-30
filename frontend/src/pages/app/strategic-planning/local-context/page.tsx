'use client';

import { useState, useEffect } from 'react';
import { 
  Globe, 
  TrendingUp, 
  MapPin,
  Lightbulb,
  ArrowUp,
  ArrowDown
} from '@/icons/nexture';
import { SPCard, SPLoading } from '@/components/strategic-planning';
import { useStrategicPlanning } from '@/context/StrategicPlanningContext';

export default function LocalContextPage() {
  const { getLocalContextForSWOT, analyzeLearningPotential, getEnhancedLocalCategories } = useStrategicPlanning();
  const [loading, setLoading] = useState(true);
  const [localContextData, setLocalContextData] = useState<any>(null);
  const [learningPotential, setLearningPotential] = useState<any>(null);
  const [categories, setCategories] = useState<any>(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    try {
      const schoolId = 'default-school-id';
      
      const [contextData, potentialData, categoriesData] = await Promise.all([
        getLocalContextForSWOT(schoolId),
        analyzeLearningPotential(schoolId),
        getEnhancedLocalCategories(schoolId)
      ]);

      setLocalContextData(contextData);
      setLearningPotential(potentialData);
      setCategories(categoriesData);
    } catch (error) {
      console.error('Error loading local context data:', error);
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
        <h1 className="text-2xl font-bold text-gray-900">Pemetaan Potensi Daerah</h1>
        <p className="text-gray-600 mt-1">Integrasi konteks lokal untuk perencanaan strategis berbasis kearifan lokal</p>
      </div>

      {/* Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <SPCard
          icon={<Globe className="w-5 h-5" />}
          title="Total Konteks Lokal"
          value={localContextData?.local_contexts?.length || 0}
          subtitle="Konteks aktif"
        />
        <SPCard
          icon={<TrendingUp className="w-5 h-5" />}
          title="Skor Potensi"
          value={learningPotential?.overall_potential_score || 0}
          subtitle="Skor pembelajaran"
        />
        <SPCard
          icon={<MapPin className="w-5 h-5" />}
          title="Cakupan Area"
          value="3 Desa"
          subtitle="Bonerate & sekitarnya"
        />
        <SPCard
          icon={<Lightbulb className="w-5 h-5" />}
          title="Peluang Integrasi"
          value="High"
          subtitle="Potensi pengembangan"
        />
      </div>

      {/* Learning Potential Analysis */}
      <SPCard title="Analisis Potensi Pembelajaran">
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <span className="text-sm text-gray-600">Skor Potensi Overall</span>
            <span className="text-2xl font-bold text-purple-600">
              {learningPotential?.overall_potential_score || 0}
            </span>
          </div>
          <div className="space-y-3">
            {learningPotential?.category_scores?.map((category: any) => (
              <div key={category.category} className="p-4 bg-gray-50 rounded-lg">
                <div className="flex items-center justify-between mb-2">
                  <h3 className="font-semibold">{category.category}</h3>
                  <span className={`px-2 py-1 rounded text-xs font-medium ${
                    category.potential === 'HIGH' ? 'bg-green-100 text-green-800' :
                    category.potential === 'MEDIUM' ? 'bg-yellow-100 text-yellow-800' :
                    'bg-red-100 text-red-800'
                  }`}>
                    {category.potential}
                  </span>
                </div>
                <div className="grid grid-cols-3 gap-4 text-sm">
                  <div>
                    <p className="text-gray-600">Skor</p>
                    <p className="font-semibold">{category.score}</p>
                  </div>
                  <div>
                    <p className="text-gray-600">Utilisasi</p>
                    <p className="font-semibold">{category.utilization}%</p>
                  </div>
                  <div>
                    <p className="text-gray-600">Gap</p>
                    <p className="font-semibold text-red-600">{category.gap}%</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </SPCard>

      {/* SWOT Integration */}
      <SPCard title="Integrasi SWOT dengan Konteks Lokal">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* Strengths */}
          <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
            <h3 className="font-semibold text-green-800 mb-3 flex items-center gap-2">
              <ArrowUp className="w-4 h-4" />
              Strengths
            </h3>
            <div className="space-y-2">
              {localContextData?.swot_integration?.strengths?.map((item: any) => (
                <div key={item.id} className="text-sm">
                  <p className="font-medium">{item.title}</p>
                  <p className="text-gray-600">{item.description}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Weaknesses */}
          <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
            <h3 className="font-semibold text-red-800 mb-3 flex items-center gap-2">
              <ArrowDown className="w-4 h-4" />
              Weaknesses
            </h3>
            <div className="space-y-2">
              {localContextData?.swot_integration?.weaknesses?.map((item: any) => (
                <div key={item.id} className="text-sm">
                  <p className="font-medium">{item.title}</p>
                  <p className="text-gray-600">{item.description}</p>
                </div>
              ))}
              {localContextData?.swot_integration?.weaknesses?.length === 0 && (
                <p className="text-sm text-gray-500">Tidak ada weaknesses teridentifikasi</p>
              )}
            </div>
          </div>

          {/* Opportunities */}
          <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
            <h3 className="font-semibold text-blue-800 mb-3 flex items-center gap-2">
              <Lightbulb className="w-4 h-4" />
              Opportunities
            </h3>
            <div className="space-y-2">
              {localContextData?.swot_integration?.opportunities?.map((item: any) => (
                <div key={item.id} className="text-sm">
                  <p className="font-medium">{item.title}</p>
                  <p className="text-gray-600">{item.description}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Threats */}
          <div className="p-4 bg-orange-50 border border-orange-200 rounded-lg">
            <h3 className="font-semibold text-orange-800 mb-3 flex items-center gap-2">
              <AlertTriangle className="w-4 h-4" />
              Threats
            </h3>
            <div className="space-y-2">
              {localContextData?.swot_integration?.threats?.map((item: any) => (
                <div key={item.id} className="text-sm">
                  <p className="font-medium">{item.title}</p>
                  <p className="text-gray-600">{item.description}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </SPCard>

      {/* Enhanced Categories */}
      <SPCard title="Kategori Lokal yang Di-Enhance">
        <div className="space-y-4">
          {categories?.map((category: any) => (
            <div key={category.category_code} className="p-4 border border-gray-200 rounded-lg">
              <div className="flex items-center justify-between mb-2">
                <h3 className="font-semibold">{category.category_name}</h3>
                <span className={`px-2 py-1 rounded text-xs font-medium ${
                  category.integration_type === 'STRONG' ? 'bg-purple-100 text-purple-800' :
                  'bg-blue-100 text-blue-800'
                }`}>
                  {category.integration_type}
                </span>
              </div>
              <p className="text-sm text-gray-600 mb-2">{category.description}</p>
              <div className="flex flex-wrap gap-2">
                {category.strategic_tags.map((tag: string) => (
                  <span key={tag} className="px-2 py-1 bg-gray-100 text-gray-700 rounded text-xs">
                    {tag}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>
      </SPCard>

      {/* Recommendations */}
      <SPCard title="Rekomendasi Strategis">
        <div className="space-y-2">
          {learningPotential?.recommendations?.map((rec: string, index: number) => (
            <div key={index} className="flex items-start gap-2 p-3 bg-purple-50 rounded-lg">
              <span className="text-purple-600 font-bold">{index + 1}.</span>
              <p className="text-sm">{rec}</p>
            </div>
          ))}
        </div>
      </SPCard>
    </div>
  );
}