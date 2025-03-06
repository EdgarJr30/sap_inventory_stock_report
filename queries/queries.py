GET_ARTICLES_NO_STOCK_PENDING_ORDERS = """
SELECT
	T2."DocDate" AS "Fecha de la orden"
	,T2."DocEntry" AS "ID interno de la orden"
	,T0."Ticket"
	,T0."Father" AS "Artículo padre"
	,T3."ItemCode" AS "Artículo hijo"
	,T0."Description" AS "Descripción"
	,T0."Ordered" AS "Cantidad Ordenada"
	,T0."OnHand"
	,T0."IsCommited" AS "Comprometido"
	,T0."OnOrder" AS "Pedido"
	,T0."Available" AS "Disponible"
	,T0."Warehouse" AS "Almacén"
	,T0."Error"
FROM
	"CEODO_VW_DST_ArtSinInv" T0
	INNER JOIN (SELECT DISTINCT 
					TC."U_WHS", 
					TC."U_BRANCH" 
				FROM 
					"@ADTS_POS_CONF" TC
				) T1 ON T1."U_WHS" = T0."Warehouse"
	INNER JOIN ORDR T2 ON T0."Ticket" = T2."U_DST_NOTICKET" AND T2."U_DST_SUCURSAL" = T1. "U_BRANCH" AND T2."DocStatus" = 'O'
	INNER JOIN OITM T3 ON T0."Child" = T3."ItemCode"
	WHERE T2."DocDate" > '2024-10-01'
ORDER BY
	5, 1
 """

CEODO_VW_DST_ArtSinInv_SalesKit = """
SELECT
	T2."DocDate" AS "Fecha de la orden"
	,T2."DocEntry" AS "ID interno de la orden"
	,T0."Ticket"
	,T0."Father" AS "Artículo padre"
	,T3."ItemCode" AS "Artículo hijo"
	,T0."Description" AS "Descripción"
	,T0."Ordered" AS "Cantidad Ordenada"
	,T0."OnHand"
	,T0."IsCommited" AS "Comprometido"
	,T0."OnOrder" AS "Pedido"
	,T0."Available" AS "Disponible"
	,T0."Warehouse" AS "Almacén"
	,T0."Error"
FROM
	"CEODO_VW_DST_ArtSinInv_SalesKit" T0
	INNER JOIN (SELECT DISTINCT 
					TC."U_WHS", 
					TC."U_BRANCH" 
				FROM 
					"@ADTS_POS_CONF" TC
				) T1 ON T1."U_WHS" = T0."Warehouse"
	INNER JOIN ORDR T2 ON T0."Ticket" = T2."U_DST_NOTICKET" AND T2."U_DST_SUCURSAL" = T1. "U_BRANCH" AND T2."DocStatus" = 'O'
	INNER JOIN OITM T3 ON T0."Child" = T3."ItemCode"
ORDER BY
	5, 1
 """

# # Para pruebas de desarrollo
# GET_ARTICLES_NO_STOCK_PENDING_ORDERS = """
# SELECT TOP 1 * FROM OINV
#  """