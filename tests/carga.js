import http from 'k6/http';
import { check, sleep } from 'k6';

const MODE = __ENV.MODE || 'normal';
const BASE_URL = __ENV.BASE_URL || 'http://localhost:8088';
const target = MODE === 'slow' ? '/slow?ms=500' : '/';
export const options = {
  stages: [
    { duration: '30s', target: 5 },
    { duration: '60s', target: 20 },
    { duration: '60s', target: 40 },
    { duration: '30s', target: 0 },
  ],
  thresholds: { http_req_failed: ['rate<0.01'], http_req_duration: ['p(95)<2000'] },
  summaryTrendStats: ['avg', 'min', 'med', 'max', 'p(90)', 'p(95)', 'p(99)'],
};
export default function () {
  const res = http.get(`${BASE_URL}${target}`, {timeout: '30s'});
  check(res, { 'HTTP 200': r => r.status === 200, 'backend identificable': r => /server [123]/.test(r.body) });
  sleep(.1);
}
