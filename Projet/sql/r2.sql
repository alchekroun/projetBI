SELECT d.name,  COUNT(*)
FROM sector as s
INNER JOIN industry as d ON s.id =  d.sectorid
INNER JOIN profile as p ON d.id = p.industryid
INNER JOIN instrument as i ON p.instrumentid = i.id
WHERE i.name IN (
	"Vivendi SA",
	"Vinci SA",
	"BNP PARIBAS",
	"Orange",
	"Sanofi",
	"COMPASS GROUP PLC",
	"BARCLAYS PLC",
	"SAP AG",
	"NESTLE SA-REG",
	"ENI SPA",
	"NVIDIA CORP",
	"AMAZON.COM INC",
	"CINTAS CORP",
	"GOLDMAN SACHS GROUP INC",
	"PEPSICO INC",
	"NXP Semiconductors N.V.",
	"CANON INC",
	"Asahi Group Holdings Ltd",
	"TOYOTA INDUSTRIES CORP",
	"KIKKOMAN CORP"
) GROUP BY d.name