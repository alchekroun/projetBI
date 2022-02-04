SELECT c.name, COUNT(*)
FROM country as c
INNER JOIN profile as p ON c.id = p.countryid
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
) GROUP BY c.name