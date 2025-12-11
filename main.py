import math
import random
from datetime import datetime

import flet as ft

# Monte Carlo π 可視化アプリ (Flet)
# 単位正方形 [-1,1]x[-1,1] に乱数で点を打ち、円内ヒット率から π を推定。
# Zabbix 連携はこの推定値を zabbix_sender などで送れば再利用できる。


BATCH_SIZE = 500        # 1ティックあたりの打点数
MAX_POINTS = 800        # グラフに保持する最新データ点数


def main(page: ft.Page) -> None:
    page.title = "Monte Carlo π visualizer (Flet)"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.padding = 20
    page.window_min_width = 640
    page.window_min_height = 540

    # 状態
    running = False
    hits = 0
    total = 0
    start_time: datetime | None = None

    # UIパーツ
    pi_text = ft.Text("π ≈ --", size=26, weight=ft.FontWeight.BOLD)
    samples_text = ft.Text("samples: 0", size=16)
    runtime_text = ft.Text("elapsed: 0 s", size=16)

    # 折れ線グラフ（推定値の推移）
    series = ft.LineChartData(
        data_points=[],
        stroke_width=2,
        color=ft.colors.BLUE,
        curved=True,
    )
    chart = ft.LineChart(
        data_series=[series],
        min_y=3.0,
        max_y=3.3,
        min_x=0,
        max_x=1000,
        animate=300,
        expand=True,
        tooltip_bgcolor=ft.colors.with_opacity(0.9, ft.colors.BLACK),
        left_axis=ft.ChartAxis(labels_size=40),
        bottom_axis=ft.ChartAxis(labels_size=30),
        horizontal_grid_lines=ft.ChartGridLines(
            color=ft.colors.with_opacity(0.08, ft.colors.BLACK)
        ),
        vertical_grid_lines=ft.ChartGridLines(
            color=ft.colors.with_opacity(0.08, ft.colors.BLACK)
        ),
    )

    def update_labels(est_pi: float | None = None) -> None:
        """テキスト類の更新"""
        nonlocal hits, total, start_time
        if est_pi is not None:
            pi_text.value = f"π ≈ {est_pi:.6f}"
        samples_text.value = f"samples: {total:,}"
        if start_time:
            runtime_text.value = f"elapsed: {(datetime.now() - start_time).total_seconds():.1f} s"
        page.update()

    def toggle_run(_: ft.ControlEvent) -> None:
        """計測の開始/停止"""
        nonlocal running, start_time
        running = not running
        if running and start_time is None:
            start_time = datetime.now()
        start_btn.icon = ft.icons.PAUSE if running else ft.icons.PLAY_ARROW
        start_btn.text = "Stop" if running else "Start"
        page.update()

    def reset(_: ft.ControlEvent) -> None:
        """計測をリセット"""
        nonlocal hits, total, running, start_time
        running = False
        hits = 0
        total = 0
        start_time = None
        series.data_points = []
        chart.max_x = 1000
        start_btn.icon = ft.icons.PLAY_ARROW
        start_btn.text = "Start"
        update_labels(None)
        chart.update()

    def on_tick(_: ft.TimerEvent) -> None:
        """タイマーごとに打点をまとめて実行"""
        nonlocal hits, total, running
        if not running:
            return

        for _ in range(BATCH_SIZE):
            x = random.uniform(-1.0, 1.0)
            y = random.uniform(-1.0, 1.0)
            total += 1
            if x * x + y * y <= 1.0:
                hits += 1

        est = 4 * hits / total
        # グラフ更新：最新の total を x として推定値を plot
        series.data_points.append(ft.LineChartDataPoint(total, est))
        if len(series.data_points) > MAX_POINTS:
            series.data_points = series.data_points[-MAX_POINTS:]
        chart.max_x = max(chart.max_x, total)

        update_labels(est)
        chart.update()

    # ボタン
    start_btn = ft.ElevatedButton(
        "Start",
        icon=ft.icons.PLAY_ARROW,
        on_click=toggle_run,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=6)),
    )
    reset_btn = ft.TextButton("Reset", on_click=reset)

    # タイマー（10Hz）
    timer = ft.Timer(interval=0.1, on_tick=on_tick)

    page.add(
        ft.Row([pi_text], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([samples_text, runtime_text], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, width=460),
        ft.Row([start_btn, reset_btn], spacing=10),
        chart,
        timer,
        ft.Text(
            "Hint: Webモードに切り替えるには `flet run --web main.py`。"
            " サーバーに送りたいときは zabbix_sender で est を送信してください。",
            size=13,
            color=ft.colors.GREY,
        ),
    )


if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER)
