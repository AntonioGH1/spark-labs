from pyspark.sql import SparkSession

if __name__ == "__main__":
    # Crear sesión de Spark
    spark = SparkSession\
        .builder\
        .appName("steam_games")\
        .getOrCreate()
    
    # Cargar el dataset
    path_games = "games_data.csv"
    df_games = spark.read.csv(path_games, header=True, inferSchema=True)
    
    # 
    df_games.createOrReplaceTempView("games")
    
    # Filtrar juegos por SO
    query = """
        SELECT id, title, release_date, developer, publisher, genres, price, overall_review, reviews
        FROM games
        WHERE mac_support = 1
        ORDER BY reviews DESC
    """
    df_filtered = spark.sql(query)
    
    # Mostrar algunos resultados
    df_filtered.show(30)
    
    # Guardar los resultados en formato JSON
    df_filtered.write.mode("overwrite").json("results/steam_games_mac")
    
    # Cerrar sesión de Spark
    spark.stop()
