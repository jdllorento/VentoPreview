import folium
from folium.plugins import HeatMap
from visualization.colormap import create_colormap

def create_topsis_map(df, lat_col="lat", lon_col="lon", score_col="score"):
    m = folium.Map(location=[df[lat_col].mean(), df[lon_col].mean()], zoom_start=11)

    colormap = create_colormap(df[score_col])

    # Marcadores con color por score
    for _, row in df.iterrows():
        folium.CircleMarker(
            location=[row[lat_col], row[lon_col]],
            radius=5,
            fill=True,
            fill_color=colormap(row[score_col]),
            color=None,
            fill_opacity=1,
            popup=f"{row['nombre']}<br>Score: {row[score_col]:.3f}",
            tooltip=row["nombre"]
        ).add_to(m)

    # Heatmap
    heat_data = df[[lat_col, lon_col, score_col]].values.tolist()
    HeatMap(
        heat_data,
        radius=35,
        blur=25,
        min_opacity=0.3,
        gradient={
            0.0: "red",
            0.5: "yellow",
            1.0: "green"
        }
    ).add_to(m)

    # Leyenda
    legend_html = """
    <div style="
        position: fixed; 
        bottom: 40px; left: 40px; width: 160px; height: 180px; 
        background-color: white; 
        border:2px solid grey; 
        z-index:9999; 
        font-size:14px;
        border-radius: 8px;
        padding: 10px;
    ">
    <strong>Rating de Viabilidad</strong><br>
    <div style="display: flex; flex-direction: column; margin-top: 10px;">

    <div style="display: flex; align-items: center;">
    <div style="background: red; width: 25px; height: 15px;"></div>
    &nbsp; Muy baja
    </div>

    <div style="display: flex; align-items: center;">
    <div style="background: yellow; width: 25px; height: 15px;"></div>
    &nbsp; Baja
    </div>

    <div style="display: flex; align-items: center;">
    <div style="background: lime; width: 25px; height: 15px;"></div>
    &nbsp; Media
    </div>

    <div style="display: flex; align-items: center;">
    <div style="background: cyan; width: 25px; height: 15px;"></div>
    &nbsp; Alta
    </div>

    <div style="display: flex; align-items: center;">
    <div style="background: blue; width: 25px; height: 15px;"></div>
    &nbsp; Muy alta
    </div>

    </div>
    </div>
    """

    m.get_root().html.add_child(folium.Element(legend_html))

    colormap.add_to(m)
    return m
