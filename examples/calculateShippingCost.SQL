-- EXAMPLE OF HOW THIS WORKS IN MY ECOM PLATFORM DB. HOW THE SERVER GETS THE INFORMATION

CREATE OR REPLACE FUNCTION calculateShippingCost(
    country TEXT,
    weightG NUMERIC,
    heightCm NUMERIC,
    widthCm NUMERIC,
    lengthCm NUMERIC
) RETURNS TABLE (
    shippingMethodName TEXT,
    estimatedShippingCost NUMERIC
) AS $$
DECLARE
    countryId UUID;
    dimensionalWeightG NUMERIC;
BEGIN
    -- Get the country ID from the countries table
    SELECT id INTO countryId
    FROM public."countries"
    WHERE name = country
    LIMIT 1;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Country not found: %', country;
    END IF;

    -- Calculate the dimensional weight (volume) in grams
    dimensionalWeightG := (heightCm * widthCm * lengthCm) / 6000; -- Assuming cm3 to dimensional weight conversion

    -- Return the estimated shipping cost for each valid shipping method for the country
    RETURN QUERY
    SELECT 
        sm."name" AS shippingMethodName,
        CASE 
            -- If the shipping cost calculation type is "Weight"
            WHEN sm."shippingCostCalculationType" = 'Weight' THEN 
                -- Use the actual weight
                weightG * sm."rateCnyPerG"
            -- If the shipping cost calculation type is "Volumetric"
            WHEN sm."shippingCostCalculationType" = 'Volumetric' THEN
                dimensionalWeightG * sm."rateCnyPerG"
            -- If the shipping cost calculation type is "Greater Weight", use the larger of actual or dimensional weight
            WHEN sm."shippingCostCalculationType" = 'Greater Weight' THEN
                GREATEST(weightG, dimensionalWeightG) * sm."rateCnyPerG"
            ELSE 
                0 -- Handle any unsupported calculation types
        END AS estimatedShippingCost
    FROM public."shippingMethods" sm
    JOIN public."shippingMethodCountries" smc ON sm."id" = smc."shippingMethodId"
    WHERE smc."countryId" = countryId
    AND (weightG BETWEEN COALESCE(sm."minimumWeightG", 0) AND COALESCE(sm."maximumWeightG", weightG + 1));
    
END;
$$ LANGUAGE plpgsql;