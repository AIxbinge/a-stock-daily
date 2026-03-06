import { BrowserRouter, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import { ConfigProvider } from 'antd';
import { 
  HomeOutlined, 
  BarChartOutlined, 
  UserOutlined 
} from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import HomePage from './pages/HomePage';
import StockPage from './pages/StockPage';
import RankingPage from './pages/RankingPage';

const BottomNav: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  
  const navItems = [
    { key: '/', icon: <HomeOutlined />, label: '首页' },
    { key: '/ranking', icon: <BarChartOutlined />, label: '排行' },
    { key: '/profile', icon: <UserOutlined />, label: '我的' },
  ];
  
  const activeKey = location.pathname === '/ranking' ? '/ranking' : '/';
  
  return (
    <div style={{
      height: 60,
      background: '#fff',
      borderTop: '1px solid #e8e8e8',
      display: 'flex',
      justifyContent: 'space-around',
      alignItems: 'center',
      position: 'fixed',
      bottom: 0,
      left: 0,
      right: 0,
      zIndex: 100,
    }}>
      {navItems.map((item) => (
        <div
          key={item.key}
          onClick={() => navigate(item.key)}
          style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            cursor: 'pointer',
            color: activeKey === item.key ? '#1890FF' : '#999',
          }}
        >
          <span style={{ fontSize: 20 }}>{item.icon}</span>
          <span style={{ fontSize: 12, marginTop: 4 }}>{item.label}</span>
        </div>
      ))}
    </div>
  );
};

const AppContent: React.FC = () => {
  return (
    <div style={{ height: '100vh', display: 'flex', flexDirection: 'column' }}>
      <div style={{ flex: 1, overflow: 'auto', paddingBottom: 60 }}>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/stock/:code" element={<StockPage />} />
          <Route path="/ranking" element={<RankingPage />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </div>
      <BottomNav />
    </div>
  );
};

const App: React.FC = () => {
  return (
    <ConfigProvider
      theme={{
        token: {
          colorPrimary: '#1890FF',
        },
      }}
    >
      <BrowserRouter>
        <AppContent />
      </BrowserRouter>
    </ConfigProvider>
  );
};

export default App;
