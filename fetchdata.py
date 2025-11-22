import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime, timedelta
import pytz

# CẤU HÌNH
SYMBOL = "BTCUSDm" 
TIMEFRAME = mt5.TIMEFRAME_M1
YEARS_BACK = 8

# 1. Kết nối MT5
print(f"[1] Connecting to MT5...")
if not mt5.initialize():
    print(f"Error: MT5 Init Failed. Code: {mt5.last_error()}")
    quit()

# 2. Tính toán thời gian (Múi giờ UTC)
timezone = pytz.timezone("Etc/UTC")
date_to = datetime.now(timezone)
date_from = date_to - timedelta(days=365 * YEARS_BACK)

print(f"[2] Fetching {SYMBOL} from {date_from.date()} to {date_to.date()}...")

# 3. Lấy dữ liệu (Dùng copy_rates_range cho khoảng thời gian dài)
rates = mt5.copy_rates_range(SYMBOL, TIMEFRAME, date_from, date_to)

# 4. Ngắt kết nối
mt5.shutdown()

# 5. Xử lý dữ liệu
if rates is None or len(rates) == 0:
    print("Error: No data found. Check symbol name or 'Max bars' setting.")
else:
    # Tạo DataFrame
    df = pd.DataFrame(rates)
    
    # Convert timestamp sang dạng đọc được
    df['time'] = pd.to_datetime(df['time'], unit='s')
    
    # Đổi tên cột cho đẹp (tuỳ chọn)
    df.rename(columns={'tick_volume': 'volume', 'real_volume': 'vol_real'}, inplace=True)

    print(f"\n✅ SUCCESS! Fetched {len(df)} candles.")
    print(f"Start: {df.iloc[0]['time']}")
    print(f"End:   {df.iloc[-1]['time']}")
    
    # Lưu file
    file_path = "Downloads/BTCUSDm_8Y_M1.csv"
    # Đảm bảo thư mục tồn tại hoặc dùng try/except
    try:
        df.to_csv(file_path, index=False)
        print(f"File saved to: {file_path}")
    except OSError:
        # Fallback nếu thư mục chưa được tạo
        df.to_csv("BTCUSDm_8Y_M1.csv", index=False)
        print("Folder not found. Saved to current directory as 'BTCUSDm_8Y_M1.csv'")