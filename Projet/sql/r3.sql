SELECT i.name
FROM instrument as i
INNER JOIN country as c ON p.instrumentid = i.id
INNER JOIN profile as p ON c.id = p.countryid
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
) AND c.name LIKE "NETHER%"