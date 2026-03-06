import { useState, useEffect } from 'react';
import { Card, Row, Col, Progress, Spin, Typography } from 'antd';
import { ArrowUpOutlined, ArrowDownOutlined } from '@ant-design/icons';
import { marketAPI, type MarketIndex } from '../services/api';

const { Text } = Typography;

const MarketCard: React.FC<{ index: MarketIndex; main?: boolean }> = ({ index, main = false }) => {
  const isUp = index.change >= 0;
  
  return (
    <Card
      style={{
        background: main ? 'linear-gradient(135deg, #1890FF 0%, #096DD9 100%)' : '#fff',
        border: main ? 'none' : '1px solid #e8e8e8',
        borderRadius: 12,
      }}
      bodyStyle={{ padding: main ? 24 : 16 }}
    >
      <div style={{ color: main ? '#fff' : '#262626' }}>
        <Text style={{ color: main ? 'rgba(255,255,255,0.8)' : '#8c8c8c', fontSize: 14 }}>
          {index.name}
        </Text>
        <div style={{ 
          fontSize: main ? 36 : 24, 
          fontWeight: 'bold',
          fontFamily: 'DIN Alternate, sans-serif',
          margin: '8px 0'
        }}>
          {index.current.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
        </div>
        <div style={{ 
          fontSize: main ? 18 : 14,
          display: 'flex',
          alignItems: 'center',
          gap: 4
        }}>
          {isUp ? <ArrowUpOutlined /> : <ArrowDownOutlined />}
          {Math.abs(index.change).toFixed(2)} 
          <span style={{ marginLeft: 8 }}>({isUp ? '+' : ''}{index.changePercent.toFixed(2)}%)</span>
        </div>
      </div>
    </Card>
  );
};

const HomePage: React.FC = () => {
  const [marketData, setMarketData] = useState<MarketIndex[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const data = await marketAPI.getMarket();
        setMarketData(data);
      } catch (error) {
        console.error('Failed to fetch market data:', error);
        // Mock data for demo
        setMarketData([
          { code: '000001', name: '上证指数', current: 3245.67, change: 39.52, changePercent: 1.23, volume: 456789000, amount: 45678900000, open: 3210.00, high: 3260.00, low: 3200.00 },
          { code: '399001', name: '深证成指', current: 11234.56, change: 98.76, changePercent: 0.89, volume: 567890000, amount: 56789000000, open: 11150.00, high: 11300.00, low: 11100.00 },
          { code: '399006', name: '创业板指', current: 2156.78, change: 45.67, changePercent: 2.17, volume: 234567000, amount: 23456700000, open: 2120.00, high: 2170.00, low: 2100.00 },
        ]);
      } finally {
        setLoading(false);
      }
    };
    
    fetchData();
  }, []);

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: 100 }}>
        <Spin size="large" />
      </div>
    );
  }

  const upCount = 3245;
  const downCount = 1523;
  const flatCount = 234;
  const total = upCount + downCount + flatCount;

  const hotSectors = [
    { name: '半导体', change: 3.45 },
    { name: '新能源', change: 2.87 },
    { name: '金融', change: 1.23 },
  ];

  return (
    <div style={{ padding: 16, background: '#f5f5f5', minHeight: '100vh' }}>
      {/* Main Index */}
      {marketData[0] && <MarketCard index={marketData[0]} main />}
      
      {/* Sub Indices */}
      <Row gutter={[12, 12]} style={{ marginTop: 12 }}>
        {marketData.slice(1).map((index) => (
          <Col span={12} key={index.code}>
            <MarketCard index={index} />
          </Col>
        ))}
      </Row>

      {/* Market Overview */}
      <Card title="市场概况" style={{ marginTop: 16, borderRadius: 12 }}>
        <div style={{ marginBottom: 16 }}>
          <Progress 
            percent={Math.round((upCount / total) * 100)} 
            strokeColor="#C4161B" 
            showInfo={false} 
          />
          <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: 8 }}>
            <Text type="danger">上涨 {upCount} 家</Text>
            <Text type="success">下跌 {downCount} 家</Text>
            <Text>平盘 {flatCount} 家</Text>
          </div>
        </div>
      </Card>

      {/* Hot Sectors */}
      <Card title="热门板块" style={{ marginTop: 16, borderRadius: 12 }}>
        {hotSectors.map((sector, idx) => (
          <div 
            key={idx}
            style={{ 
              padding: '12px 0', 
              borderBottom: idx < hotSectors.length - 1 ? '1px solid #f0f0f0' : 'none',
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center'
            }}
          >
            <Text>{sector.name}</Text>
            <Text type={sector.change > 0 ? 'danger' : 'success'}>
              {sector.change > 0 ? '+' : ''}{sector.change.toFixed(2)}%
            </Text>
          </div>
        ))}
      </Card>
    </div>
  );
};

export default HomePage;
