import { useState, useEffect } from 'react';
import { Card, Tabs, Table, Tag, Spin, Typography, Row, Col } from 'antd';
import { useNavigate } from 'react-router-dom';
import { marketAPI, type RankingItem } from '../services/api';

const { Text } = Typography;

const RankingPage: React.FC = () => {
  const navigate = useNavigate();
  const [rankingData, setRankingData] = useState<RankingItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('up');

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const data = await marketAPI.getRanking(activeTab, 50);
        setRankingData(data.items);
      } catch (error) {
        console.error('Failed to fetch ranking data:', error);
        // Mock data
        const mockData: RankingItem[] = [
          { rank: 1, code: '600519', name: '贵州茅台', current: 1678.00, change: 87.25, changePercent: 5.48, volume: 1234567, amount: 1234567890 },
          { rank: 2, code: '000858', name: '五粮液', current: 189.50, change: 8.70, changePercent: 4.82, volume: 987654, amount: 987654321 },
          { rank: 3, code: '600809', name: '山西汾酒', current: 312.80, change: 13.25, changePercent: 4.42, volume: 876543, amount: 876543210 },
          { rank: 4, code: '000596', name: '古井贡酒', current: 234.60, change: 8.90, changePercent: 3.94, volume: 765432, amount: 765432109 },
          { rank: 5, code: '002304', name: '洋河股份', current: 178.90, change: 6.50, changePercent: 3.77, volume: 654321, amount: 654321098 },
          { rank: 6, code: '603589', name: '金种子酒', current: 45.30, change: 1.35, changePercent: 3.07, volume: 543210, amount: 543210987 },
          { rank: 7, code: '603919', name: '金徽酒', current: 56.80, change: 1.65, changePercent: 2.99, volume: 432109, amount: 432109876 },
          { rank: 8, code: '600197', name: '伊力特', current: 67.50, change: 1.85, changePercent: 2.82, volume: 321098, amount: 321098765 },
          { rank: 9, code: '000569', name: '海马汽车', current: 89.20, change: 2.30, changePercent: 2.64, volume: 210987, amount: 210987654 },
          { rank: 10, code: '600059', name: '华钰矿业', current: 12.45, change: 0.30, changePercent: 2.47, volume: 109876, amount: 109876543 },
        ];
        setRankingData(mockData);
      } finally {
        setLoading(false);
      }
    };
    
    fetchData();
  }, [activeTab]);

  const columns = [
    {
      title: '排名',
      dataIndex: 'rank',
      key: 'rank',
      width: 60,
      render: (rank: number) => (
        <span style={{ 
          fontWeight: 'bold',
          color: rank <= 3 ? '#FAAD14' : '#595959'
        }}>
          {rank}
        </span>
      ),
    },
    {
      title: '股票',
      key: 'stock',
      render: (_: unknown, record: RankingItem) => (
        <div>
          <Text strong>{record.name}</Text>
          <br />
          <Text type="secondary" style={{ fontSize: 12 }}>{record.code}</Text>
        </div>
      ),
    },
    {
      title: '现价',
      dataIndex: 'current',
      key: 'current',
      width: 80,
      render: (value: number) => (
        <Text strong>{value.toFixed(2)}</Text>
      ),
    },
    {
      title: '涨跌幅',
      key: 'change',
      width: 100,
      render: (_: unknown, record: RankingItem) => (
        <Tag color={record.changePercent >= 0 ? 'red' : 'green'}>
          {record.changePercent >= 0 ? '+' : ''}{record.changePercent.toFixed(2)}%
        </Tag>
      ),
    },
  ];

  const hotConcepts = [
    { name: '白酒', change: 4.23 },
    { name: '半导体', change: 3.87 },
    { name: '新能源', change: 3.45 },
    { name: '金融', change: 2.12 },
  ];

  return (
    <div style={{ padding: 16, background: '#f5f5f5', minHeight: '100vh' }}>
      <Card style={{ borderRadius: 12, marginBottom: 16 }}>
        <Tabs 
          activeKey={activeTab} 
          onChange={setActiveTab}
          items={[
            { key: 'up', label: '涨幅榜' },
            { key: 'down', label: '跌幅榜' },
            { key: 'volume', label: '成交额' },
          ]}
        />
        
        {loading ? (
          <div style={{ textAlign: 'center', padding: 40 }}>
            <Spin />
          </div>
        ) : (
          <Table 
            columns={columns}
            dataSource={rankingData}
            rowKey="rank"
            pagination={false}
            size="small"
            onRow={(record) => ({
              onClick: () => navigate(`/stock/${record.code}`),
              style: { cursor: 'pointer' },
            })}
          />
        )}
      </Card>

      {/* Hot Concepts */}
      <Card title="热门概念" style={{ borderRadius: 12, marginBottom: 16 }}>
        <Row gutter={[12, 12]}>
          {hotConcepts.map((concept, idx) => (
            <Col span={12} key={idx}>
              <Card size="small" style={{ borderRadius: 8 }}>
                <div style={{ textAlign: 'center' }}>
                  <Text>{concept.name}</Text>
                  <div style={{ 
                    fontSize: 16, 
                    fontWeight: 'bold',
                    color: concept.change > 0 ? '#C4161B' : '#2BA540'
                  }}>
                    {concept.change > 0 ? '+' : ''}{concept.change.toFixed(2)}%
                  </div>
                </div>
              </Card>
            </Col>
          ))}
        </Row>
      </Card>
    </div>
  );
};

export default RankingPage;
