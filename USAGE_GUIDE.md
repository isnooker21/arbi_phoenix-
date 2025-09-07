# 🔥 ARBI PHOENIX - Usage Guide

## การใช้งานระบบ Arbi Phoenix ที่ปรับปรุงแล้ว

### ✨ คุณสมบัติใหม่

1. **🔗 การเชื่อมต่อโบรกเกอร์อัตโนมัติ**
   - ระบบจะเชื่อมต่อกับโบรกเกอร์โดยอัตโนมัติเมื่อเริ่มต้น
   - มีการตรวจสอบสถานะการเชื่อมต่อและเชื่อมต่อใหม่อัตโนมัติ
   - รองรับการเชื่อมต่อหลายโบรกเกอร์

2. **🖥️ GUI Dashboard ที่ทันสมัย**
   - หน้าต่างควบคุมการเทรดแบบ Real-time
   - ปุ่ม **START TRADE** สำหรับเริ่มการเทรด
   - แสดงสถิติและข้อมูลการเทรดแบบสด
   - ระบบ Activity Log แบบสี

3. **⚡ ระบบการเทรดอัตโนมัติ**
   - เริ่มการเทรดด้วยการกดปุ่มเดียว
   - ระบบ Recovery แบบหลายชั้น
   - การจัดการกำไรแบบอัตโนมัติ

---

## 🚀 การติดตั้งและเริ่มใช้งาน

### 1. ติดตั้ง Dependencies

```bash
pip install -r requirements.txt
```

### 2. ตั้งค่าโบรกเกอร์

แก้ไขไฟล์ `config/config.yaml`:

```yaml
broker:
  name: "IC_Markets"
  api_type: "MT5"
  server: "ICMarkets-Demo"
  login: "your_login_here"
  password: "your_password_here"
  auto_connect: true        # เชื่อมต่ออัตโนมัติ
  reconnect_interval: 60    # ช่วงเวลาเชื่อมต่อใหม่ (วินาที)

trading:
  auto_start: false         # เริ่มเทรดอัตโนมัติเมื่อเปิดโปรแกรม
  min_arbitrage_profit: 5   # กำไรขั้นต่ำ (pips)
  base_lot_size: 0.01       # ขนาด lot พื้นฐาน
```

### 3. เริ่มใช้งาน

```bash
python main.py
```

---

## 🎮 การใช้งาน GUI Dashboard

### หน้าจอหลัก

1. **🔥 Trading Control Panel**
   - **🚀 START TRADE**: เริ่มระบบการเทรด
   - **⏸️ PAUSE**: หยุดชั่วคราว
   - **🛑 STOP**: หยุดการเทรด
   - **Trading Mode**: เลือกโหมดการเทรด (Conservative/Balanced/Aggressive)

2. **📊 Performance Metrics**
   - **Total Profit**: กำไรรวม
   - **Opportunities**: โอกาสที่พบ
   - **Success Rate**: อัตราความสำเร็จ
   - **Active Positions**: ตำแหน่งที่เปิดอยู่

3. **📝 Activity Log**
   - แสดงกิจกรรมแบบ Real-time
   - ข้อความแบบสีตามระดับความสำคัญ
   - บันทึกการเชื่อมต่อและการเทรด

### แท็บต่างๆ

1. **🎯 Opportunities Tab**
   - แสดงโอกาส Triangular Arbitrage
   - ข้อมูลกำไรและค่าใช้จ่าย Spread
   - สถานะความพร้อมในการเทรด

2. **📈 Positions Tab**
   - ตำแหน่งการเทรดที่เปิดอยู่
   - กำไร/ขาดทุนแบบ Real-time
   - ข้อมูลเวลาและปริมาณ

3. **🔄 Recovery Tab**
   - สถานะระบบ Recovery
   - ความคืบหนา Recovery
   - ข้อมูลการฟื้นตัว

4. **📊 Charts Tab**
   - กราฟประสิทธิภาพ (จะพัฒนาต่อ)

---

## ⚙️ การตั้งค่าขั้นสูง

### การเชื่อมต่ออัตโนมัติ

```yaml
broker:
  auto_connect: true
  retries: 3
  reconnect_interval: 60
```

### การเริ่มเทรดอัตโนมัติ

```yaml
trading:
  auto_start: true  # เริ่มเทรดทันทีเมื่อเชื่อมต่อสำเร็จ
```

### การตั้งค่าระดับกำไร

```yaml
trading:
  profit_levels:
    quick_scalp: 8      # กำไรด่วน
    partial_1: 15       # กำไรระดับ 1
    partial_2: 25       # กำไรระดับ 2
    final_target: 40    # เป้าหมายสุดท้าย
  
  profit_percentages:
    quick_scalp: 25     # ปิด 25% ที่ระดับแรก
    partial_1: 25       # ปิด 25% ที่ระดับสอง
    partial_2: 30       # ปิด 30% ที่ระดับสาม
    final_target: 20    # เหลือ 20% ที่เป้าหมายสุดท้าย
```

### การตั้งค่า Recovery System

```yaml
recovery:
  max_recovery_layers: 6      # ชั้น Recovery สูงสุด
  recovery_multiplier: 1.5    # ตัวคูณขนาดตำแหน่ง
  strong_correlation: 0.8     # ความสัมพันธ์แกว่ง
  recovery_delay: 30          # หน่วงเวลาก่อน Recovery
```

---

## 🔧 การแก้ไขปัญหา

### ปัญหาการเชื่อมต่อ

1. **ตรวจสอบข้อมูลโบรกเกอร์**
   ```yaml
   broker:
     login: "เลขบัญชีที่ถูกต้อง"
     password: "รหัสผ่านที่ถูกต้อง"
     server: "เซิร์ฟเวอร์ที่ถูกต้อง"
   ```

2. **ตรวจสอบการติดตั้ง MetaTrader5**
   ```bash
   pip install MetaTrader5
   ```

3. **ดูสถานะการเชื่อมต่อใน GUI**
   - ดูที่มุมขวาบนของหน้าจอ
   - 🟢 = เชื่อมต่อสำเร็จ
   - 🔴 = เชื่อมต่อไม่สำเร็จ

### ปัญหา GUI

1. **ติดตั้ง PyQt6**
   ```bash
   pip install PyQt6 qasync
   ```

2. **ปัญหาการแสดงผล**
   - ตรวจสอบความละเอียดหน้าจอ
   - ปรับขนาดหน้าต่าง

### ปัญหาการเทรด

1. **ไม่พบโอกาส Arbitrage**
   - ลดค่า `min_arbitrage_profit`
   - เพิ่มค่า `max_spread_cost`

2. **การเทรดไม่เริ่ม**
   - ตรวจสอบการเชื่อมต่อโบรกเกอร์
   - ตรวจสอบยอดเงินในบัญชี
   - ดู Activity Log สำหรับข้อผิดพลาด

---

## 📊 การตรวจสอบประสิทธิภาพ

### ตัวชี้วัดสำคัญ

1. **Success Rate**: ควรอยู่ที่ 85%+
2. **Average Profit per Trade**: ควรมากกว่า 10 pips
3. **Recovery Rate**: ควรอยู่ที่ 90%+
4. **Connection Uptime**: ควรอยู่ที่ 99%+

### การปรับแต่งประสิทธิภาพ

1. **เพิ่มความถี่การสแกน**
   ```yaml
   gui:
     triangle_update: 250  # ลดจาก 500ms
   ```

2. **ปรับระดับความเสี่ยง**
   ```yaml
   trading:
     max_position_risk: 1.0  # ลดความเสี่ยง
   ```

---

## 🛡️ ความปลอดภัย

### การจัดการความเสี่ยง

1. **ตั้งค่า Stop Loss อัตโนมัติ**
2. **จำกัดจำนวนตำแหน่งสูงสุด**
3. **ตรวจสอบความสัมพันธ์ของสกุลเงิน**
4. **ระบบ Emergency Stop**

### การสำรองข้อมูล

1. **บันทึก Log อัตโนมัติ** ใน `data/logs/`
2. **ฐานข้อมูลการเทรด** ใน `data/phoenix.db`
3. **การตั้งค่า** ใน `config/config.yaml`

---

## 🔄 การอัปเดตระบบ

### การอัปเดต Configuration

```python
from phoenix_utils import ConfigManager

config = ConfigManager()
config.set('trading.min_arbitrage_profit', 3)
config.save()
```

### การรีสตาร์ทระบบ

1. กดปุ่ม **🛑 STOP** ใน GUI
2. ปิดโปรแกรม
3. เริ่มใหม่ด้วย `python main.py`

---

## 📞 การสนับสนุน

หากพบปัญหาหรือต้องการความช่วยเหลือ:

1. ตรวจสอบ Activity Log ใน GUI
2. ดูไฟล์ Log ใน `data/logs/`
3. ตรวจสอบการตั้งค่าใน `config/config.yaml`

---

**🔥 "The Phoenix Never Dies" 🔥**

*ระบบ Arbi Phoenix ได้รับการปรับปรุงให้ทำงานอัตโนมัติและใช้งานง่ายขึ้น พร้อมกับ GUI ที่ทันสมัยและระบบการเชื่อมต่อที่เสถียร*
