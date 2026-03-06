import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Card, Spin, Typography, Descriptions, Space } from 'antd';
import { ArrowUpOutlined, ArrowDownOutlined } from '@ant-design/icons';
import ReactECharts from 'echarts-for-react';
import { marketAPI, type StockInfo } from '../services/api';

const { Title, Text } = Typography;

const StockPage: React.FC = () => {
  const { code } = useParams<{ code: string }>();
  const [stock, setStock] = useState<StockInfo | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      if (!code) return;
      setLoading(true);
      try {
        const data = await marketAPI.getStock(code);
        setStock(data);
      } catch (error) {
        console.error('Failed to fetch stock data:', error);
        // Mock data
        setStock({
          code: code,
          name: code === '600000' ? '浦发银行' : '平安银行',
          current: 15.68,
          change: 0.35,
          changePercent: 2.28,
          open: 15.30,
          high: 15.80,
          low: 15.25,
          volume: 45678900,
          amount: 712345678,
          turnover: 1.23,
          pe: 6.78,
          pb: 0.65,
          marketCap: 45678900000,
          timestamp: new Date().toISOString(),
        });
      } finally {
        setLoading(false);
      }
    };
    
    fetchData();
  }, [code]);

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: 100 }}>
        <Spin size="large" />
      </div>
    );
  }

  if (!stock) {
    return <div style={{ padding: 16 }}>股票不存在</div>;
  }

  const isUp = stock.change >= 0;
  const mainColor = isUp ? '#C4161B' : '#2BA540';

  // K线图配置（简单模拟）
  const klineOption = {
    title: { text: '日K线' },
    tooltip: { trigger: 'axis' },
    xAxis: {
      type: 'category',
      data: ['周一', '周二', '周三', '周四', '周五'],
    },
    yAxis: { type: 'value' },
    series: [{
      type: 'candlestick',
      data: [
        [15.2, 15.5, 15.1, 15.3],
        [15.3, 15.8, 15.2, 15.6],
        [15.6, 15.9, 15.4, 15.7],
        [15.7, 16.0, 15.5, 15.8],
        [15.8, 16.2, 15.6, 15.68],
      ],
    }],
  };

  // 分时图配置
  const minuteOption = {
    title: { text: '分时走势' },
    tooltip: { trigger: 'axis' },
    xAxis: {
      type: 'category',
      data: ['09:30', '10:00', '10:30', '11:00', '11:30', '13:00', '13:30', '14:00', '14:30', '15:00'],
    },
    yAxis: { type: 'value' },
    series: [{
      type: 'line',
      data: [15.30, 15.45, 15.50, 15.60, 15.55, 15.65, 15.70, 15.62, 15.65, 15.68],
      smooth: true,
      areaStyle: {
        color: isUp ? 'rgba(196, 22, 27, 0.1)' : 'rgba(43, 165, 64, 0.1)',
      },
      lineStyle: { color: mainColor },
      itemStyle: { color: mainColor },
    }],
  };

  return (
    <div style={{ padding: 16, background: '#f5f5f5', minHeight: '100vh' }}>
      {/* Header */}
      <Card style={{ borderRadius: 12, marginBottom: 16 }}>
        <div style={{ textAlign: 'center' }}>
          <Title level={3} style={{ margin: 0 }}>{stock.name}</Title>
          <Text type="secondary">{stock.code}</Text>
        </div>
        <div style={{ textAlign: 'center', marginTop: 16 }}>
          <span style={{ fontSize: 42, fontWeight: 'bold', fontFamily: 'DIN Alternate' }}>
            {stock.current.toFixed(2)}
          </span>
          <Space style={{ marginLeft: 16, fontSize: 18 }}>
            {isUp ? <ArrowUpOutlined style={{ color: '#C4161B' }} /> : <ArrowDownOutlined style={{ color: '#2BA540' }} />}
            <Text style={{ color: mainColor }}>
              {Math.abs(stock.change).toFixed(2)} ({isUp ? '+' : ''}{stock.changePercent.toFixed(2)}%)
            </Text>
          </Space>
        </div>
      </Card>

      {/* Charts */}
      <Card title="分时走势" style={{ borderRadius: 12, marginBottom: 16 }}>
        <ReactECharts option={minuteOption} style={{ height: 250 }} />
      </Card>

      <Card title="日K线" style={{ borderRadius: 12, marginBottom: 16 }}>
        <ReactECharts option={klineOption} style={{ height: 300 }} />
      </Card>

      {/* Details */}
      <Card title="基本信息" style={{ borderRadius: 12 }}>
        <Descriptions column={2} size="small">
          <Descriptions.Item label="开盘">{stock.open.toFixed(2)}</Descriptions.Item>
          <Descriptions.Item label="最高">{stock.high.toFixed(2)}</Descriptions.Item>
          <Descriptions.Item label="最低">{stock.low.toFixed(2)}</Descriptions.Item>
          <Descriptions.Item label="成交量">{((stock.volume / 10000).toFixed(2))}万</Descriptions.Item>
          <Descriptions.Item label="成交额">{((stock.amount / 100000000).toFixed(2))}亿</Descriptions.Item>
          <Descriptions.Item label="换手率">{stock.turnover?.toFixed(2) ?? '--'}%</Descriptions.Item>
          <Descriptions.Item label="市盈率">{stock.pe?.toFixed(2) ?? '--'}</Descriptions.Item>
          <Descriptions.Item label="市净率">{stock.pb?.toFixed(2) ?? '--'}</Descriptions.Item>
        </Descriptions>
      </Card>
    </div>
  );
};

export default StockPage;
